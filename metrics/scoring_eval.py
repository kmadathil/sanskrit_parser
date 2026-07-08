#!/usr/bin/env python3
"""
Evaluate sandhi split scoring approaches using Boundary-F1 and Recall@K.

Each approach runs its own DAG search (weighted or unweighted) with max_paths=10.

Compares:
  A. Min-words: unweighted search (fewer words = better)
  B. CBOW+SP raw: CBOW-weighted search
  C. CBOW+SP normalized: CBOW/piece-weighted search
  D. Word-vector: reranker on unweighted pool (per-edge weight not feasible)
  E. Word-count primary + CBOW tiebreaker (unweighted search + rerank, default)

Usage:
  python metrics/scoring_eval.py --count 200               (limited, fast)
  python metrics/scoring_eval.py                           (all 9042 entries)
  python metrics/scoring_eval.py --max-paths 50            (wider beam)
  python metrics/scoring_eval.py --max-paths 200 --count 500
"""

import heapq, logging, os, sys, inspect, time
from collections import defaultdict

import networkx as nx
import numpy as np
import pandas as pd
from tqdm import tqdm

from indic_transliteration import sanscript
from sanskrit_parser.base.sanskrit_base import SanskritObject, outputctx
from sanskrit_parser.parser.sandhi_analyzer import LexicalSandhiAnalyzer
from sanskrit_parser.util.lexical_scorer import Scorer, gensim_enabled

BASE_DIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
DATA_DIR = os.path.join(BASE_DIR, '..', 'tests', 'SandhiKosh')
KOSH_FILE = os.path.join(DATA_DIR, 'Result.xls')

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.WARNING)
logging.getLogger('gensim').setLevel(logging.WARNING)

# ---------------------------------------------------------------------------
# Metric helpers
# ---------------------------------------------------------------------------

def split_boundaries(words):
    """Return set of character offsets where word boundaries occur.

    Given ['asti', 'uttarasyAm', 'diSi', 'devatAtmA'],
    returns {4, 15, 19} (positions in the concatenated string).
    """
    pos = 0
    boundaries = set()
    for w in words:
        pos += len(w)
        boundaries.add(pos)
    boundaries.discard(pos)  # remove end-of-string position
    return boundaries


def boundary_f1(candidate_words, reference_words):
    """Compute Boundary-F1 between candidate and reference word splits."""
    ref_bounds = split_boundaries(reference_words)
    cand_bounds = split_boundaries(candidate_words)
    true_pos = len(ref_bounds & cand_bounds)
    pred_pos = len(cand_bounds)
    actual_pos = len(ref_bounds)
    if pred_pos == 0 and actual_pos == 0:
        return 1.0
    prec = true_pos / pred_pos if pred_pos > 0 else 0.0
    rec = true_pos / actual_pos if actual_pos > 0 else 0.0
    f1 = 2 * prec * rec / (prec + rec) if (prec + rec) > 0 else 0.0
    return f1


# ---------------------------------------------------------------------------
# Weighted DAG search
# ---------------------------------------------------------------------------

def _shortest_paths_weighted(G, source, target, k, weight_map):
    """Return up to k paths from source to target, sorted by total weight.

    weight_map: dict of (u,v) -> float (smaller = better / cheaper)
    Uses topological DP with per-node beam (k).
    Returns list of (total_cost, [node, ...]) including start and end nodes.
    """
    final_paths = {node: [] for node in G.nodes()}
    temp_heaps = {node: [] for node in G.nodes()}
    final_paths[source] = [(0, None, None)]

    for u in nx.topological_sort(G):
        if u != source:
            final_paths[u] = sorted([(-c, p, idx) for c, p, idx in temp_heaps[u]])
        if not final_paths[u]:
            continue
        for v in G.successors(u):
            ew = weight_map.get((u, v), 1)
            for i, (cost, _, _) in enumerate(final_paths[u]):
                new_cost = cost + ew
                if len(temp_heaps[v]) < k:
                    heapq.heappush(temp_heaps[v], (-new_cost, u, i))
                elif new_cost < -temp_heaps[v][0][0]:
                    heapq.heapreplace(temp_heaps[v], (-new_cost, u, i))

    results = []
    for cost, parent, idx in final_paths[target]:
        path = [target]
        curr_p, curr_idx = parent, idx
        while curr_p is not None:
            path.append(curr_p)
            _, curr_p, curr_idx = final_paths[curr_p][curr_idx]
        results.append((cost, path[::-1]))
    return results


def _edge_weights_cbow_raw(G, start, end, scorer):
    """Edge weights matching original score_graph().

    start→w:  score single word [w]
    w→end:    score single word [w]
    w1→w2:    score bigram "w1 w2" (matching score_graph's tuple-as-two-words)
    Weight = -score (negative so search minimizes).
    """
    weights = {}
    for u, v in G.edges():
        if u == start:
            s = str(v)
        elif v == end:
            s = str(u)
        else:
            s = str(u) + " " + str(v)
        pieces = scorer.sp.EncodeAsPieces(s)
        raw = scorer.model.score([pieces])[0]
        weights[(u, v)] = -raw
    return weights


def _edge_weights_cbow_norm(G, start, end, scorer):
    """Edge weights = -(CBOW log-prob per piece), matching bigram scheme."""
    weights = {}
    for u, v in G.edges():
        if u == start:
            s = str(v)
        elif v == end:
            s = str(u)
        else:
            s = str(u) + " " + str(v)
        pieces = scorer.sp.EncodeAsPieces(s)
        raw = scorer.model.score([pieces])[0]
        weights[(u, v)] = -raw / max(len(pieces), 1)
    return weights


# ---------------------------------------------------------------------------
# Scoring functions
# ---------------------------------------------------------------------------

def score_min_words(path):
    """Negative word count: fewer words = higher score."""
    return -len(path)


def score_cbow_raw(paths, scorer):
    """Raw CBOW sum-of-log-probs (current score_strings)."""
    sentences = [" ".join(map(str, p)) for p in paths]
    pieces = [scorer.sp.EncodeAsPieces(s) for s in sentences]
    raw = scorer.model.score(pieces, total_sentences=len(sentences))
    return list(raw)


def score_cbow_normalized(paths, scorer):
    """CBOW score normalized by piece count (avg log-prob per piece)."""
    sentences = [" ".join(map(str, p)) for p in paths]
    pieces = [scorer.sp.EncodeAsPieces(s) for s in sentences]
    raw = scorer.model.score(pieces, total_sentences=len(sentences))
    return [s / max(len(p), 1) for s, p in zip(raw, pieces)]


def score_wordvec(paths, scorer):
    """Average cosine similarity between adjacent word vectors.

    Each word vector = average of its SentencePiece piece vectors.
    """
    scores = []
    for path in paths:
        vecs = []
        for w in path:
            word_str = str(w)
            pieces = scorer.sp.EncodeAsPieces(word_str)
            piece_vecs = [scorer.model.wv[p] for p in pieces if p in scorer.model.wv]
            if not piece_vecs:
                vecs = None
                break
            vecs.append(np.mean(piece_vecs, axis=0))
        if vecs is None or len(vecs) < 2:
            scores.append(-1.0)
            continue
        sims = []
        for i in range(len(vecs) - 1):
            v1, v2 = vecs[i], vecs[i + 1]
            n1, n2 = np.linalg.norm(v1), np.linalg.norm(v2)
            if n1 == 0 or n2 == 0:
                sims.append(0.0)
            else:
                sims.append(np.dot(v1, v2) / (n1 * n2))
        scores.append(np.mean(sims) if sims else -1.0)
    return scores


def score_wordcount_primary(paths, cbow_scores):
    """Word count primary, CBOW tiebreaker (current default)."""
    return list(zip([-len(p) for p in paths], cbow_scores))


# ---------------------------------------------------------------------------
# Evaluation
# ---------------------------------------------------------------------------

def evaluate_single(graph, ref_words, scorer, max_paths=10):
    """Run each approach with its own search and evaluate top-K.

    Returns dict of {approach_name: {pos, f1_at_1, f1_at_10, recall_at_k}}
    """
    ref_str = list(ref_words)
    results = {}

    graph.lock_start()
    G = graph.G
    start = graph.start
    end = graph.end

    if start not in G or end not in G:
        return None

    # Unit weight map for unweighted search
    unit = {(u, v): 1 for u, v in G.edges()}

    # === Unweighted search (shared base for min_words, wc_primary, wordvec) ===
    splits_full = _shortest_paths_weighted(G, start, end, max_paths, unit)
    if not splits_full:
        return None
    path_set = [[str(w) for w in p[1:-1]] for _, p in splits_full]
    # Keep inner node objects for CBOW scoring
    splits_inner = [p[1:-1] for _, p in splits_full]

    # === min_words: unweighted search, no reranking ===
    results['min_words'] = _compute_metrics(list(range(len(path_set))),
                                            path_set, ref_str)

    if not gensim_enabled:
        return results

    # === wc_primary: unweighted search + CBOW tiebreaker ===
    cbow_raw_scores = score_cbow_raw(splits_inner, scorer)
    combined = score_wordcount_primary(path_set, cbow_raw_scores)
    scored = sorted(enumerate(combined), key=lambda x: (-x[1][0], -x[1][1]))
    order = [i for i, _ in scored]
    results['wc_primary'] = _compute_metrics(order, path_set, ref_str)

    # === cbow_raw: CBOW-weighted search ===
    cbow_w = _edge_weights_cbow_raw(G, start, end, scorer)
    splits_cb = _shortest_paths_weighted(G, start, end, max_paths, cbow_w)
    path_set_cb = ([[str(w) for w in p[1:-1]] for _, p in splits_cb]
                   if splits_cb else [])
    results['cbow_raw'] = _compute_metrics(list(range(len(path_set_cb))),
                                           path_set_cb, ref_str)

    # === cbow_norm: CBOW-normalized-weighted search ===
    cbow_nw = _edge_weights_cbow_norm(G, start, end, scorer)
    splits_cn = _shortest_paths_weighted(G, start, end, max_paths, cbow_nw)
    path_set_cn = ([[str(w) for w in p[1:-1]] for _, p in splits_cn]
                   if splits_cn else [])
    results['cbow_norm'] = _compute_metrics(list(range(len(path_set_cn))),
                                            path_set_cn, ref_str)

    # === wordvec: re-ranker on the unweighted pool only ===
    # (not edge-weight compatible; needs cross-word cosine sim)
    wv_scores = score_wordvec(splits_inner, scorer)
    scored = sorted(enumerate(wv_scores), key=lambda x: -x[1])
    order = [i for i, _ in scored]
    results['wordvec'] = _compute_metrics(order, path_set, ref_str)

    return results


def _compute_metrics(order, path_strs, ref_str):
    """Compute position, recall@K, and top-K F1."""
    n = len(order)
    try:
        pos = order.index(next(i for i, p in enumerate(path_strs) if p == ref_str))
    except (StopIteration, ValueError):
        pos = None

    out = {'n_paths': n, 'pos': pos}

    for k in [1, 5, 10]:
        out[f'recall@{k}'] = 1 if pos is not None and pos < k else 0

    # Top-1 F1
    if n > 0:
        best = path_strs[order[0]]
        out['f1_at_1'] = boundary_f1(best, ref_str)
    else:
        out['f1_at_1'] = 0.0

    # Top-10 F1 (best among first 10)
    best_f1 = 0.0
    for rank in range(min(10, n)):
        cand = path_strs[order[rank]]
        f1 = boundary_f1(cand, ref_str)
        best_f1 = max(best_f1, f1)
    out['f1_at_10'] = best_f1

    return out


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def load_kosh(count=None):
    """Load sandhi kosha entries."""
    kosh = pd.read_excel(KOSH_FILE)
    passing = kosh[kosh['Status'] == 'Pass']
    if count:
        passing = passing.head(count)
    entries = []
    for _, row in passing.iterrows():
        word = row['Word']
        split_str = row['Split'].strip().replace(' ', '+')
        ref_split = [SanskritObject(x, encoding=sanscript.DEVANAGARI,
                                    strict_io=True,
                                    replace_ending_visarga=None).canonical()
                     for x in split_str.split('+')]
        entries.append({
            'word': word,
            'word_slp': SanskritObject(word, encoding=sanscript.DEVANAGARI,
                                       strict_io=True,
                                       replace_ending_visarga=None).canonical(),
            'ref': ref_split,
        })
    return entries


def main(count=None, max_paths=10):
    entries = load_kosh(count)
    logger.info("Loaded %d kosh entries, max_paths=%d", len(entries), max_paths)

    anal = LexicalSandhiAnalyzer()
    scorer = Scorer() if gensim_enabled else None

    # Accumulate per-approach stats
    stats = defaultdict(lambda: {
        'count': 0, 'found': 0, 'recall_1': 0, 'recall_5': 0,
        'recall_10': 0, 'sum_pos': 0,
        'sum_f1_1': 0.0, 'sum_f1_10': 0.0,
    })

    skipped = 0
    start = time.time()

    with outputctx(False):
        for i, ent in enumerate(tqdm(entries)):
            s = SanskritObject(ent['word'], encoding=sanscript.DEVANAGARI,
                               strict_io=True, replace_ending_visarga=None)
            graph = anal.getSandhiSplits(s)
            if graph is None:
                skipped += 1
                continue

            result = evaluate_single(graph, ent['ref'], scorer, max_paths=max_paths)
            if result is None:
                skipped += 1
                continue

            for approach, metrics in result.items():
                s = stats[approach]
                s['count'] += 1
                if metrics['pos'] is not None:
                    s['found'] += 1
                    s['recall_1'] += metrics['recall@1']
                    s['recall_5'] += metrics['recall@5']
                    s['recall_10'] += metrics['recall@10']
                    s['sum_pos'] += metrics['pos']
                s['sum_f1_1'] += metrics['f1_at_1']
                s['sum_f1_10'] += metrics['f1_at_10']

            if (i + 1) % 200 == 0:
                elapsed = time.time() - start
                logger.info("Processed %d/%d (%.1f/s)", i + 1, len(entries),
                            (i + 1) / elapsed)

    elapsed = time.time() - start
    logger.info("Done. Took %.1fs (%d entries, %d skipped)", elapsed,
                len(entries), skipped)

    # Print report
    print()
    print("=" * 78)
    print(f"{'Approach':<20} {'Recall@1':>9} {'Recall@5':>9} {'Recall@10':>9} "
          f"{'F1@1':>7} {'F1@10':>7} {'AvgPos':>7} {'Found':>6}")
    print("-" * 78)
    for approach in ['min_words', 'cbow_raw', 'cbow_norm', 'wordvec', 'wc_primary']:
        if approach not in stats:
            continue
        s = stats[approach]
        c = s['count']
        r1 = s['recall_1'] / c * 100 if c else 0
        r5 = s['recall_5'] / c * 100 if c else 0
        r10 = s['recall_10'] / c * 100 if c else 0
        f1_1 = s['sum_f1_1'] / c * 100 if c else 0
        f1_10 = s['sum_f1_10'] / c * 100 if c else 0
        avg_pos = s['sum_pos'] / s['found'] if s['found'] else 0
        found_pct = s['found'] / c * 100 if c else 0
        print(f"{approach:<20} {r1:>8.1f}% {r5:>8.1f}% {r10:>8.1f}% "
              f"{f1_1:>6.1f}% {f1_10:>6.1f}% "
              f"{avg_pos:>6.1f}  {found_pct:>5.1f}%")
    print("=" * 78)

    # Also report not-found-in-graph
    print(f"\nSkipped (no graph): {skipped} / {len(entries)}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format="%(levelname)s:%(name)s:%(message)s")
    import argparse
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--count', type=int, default=None,
                   help='Limit to N entries')
    p.add_argument('--max-paths', '-k', type=int, default=10,
                   help='Beam width / number of paths per approach (default: 10)')
    args = p.parse_args()
    main(args.count, args.max_paths)
