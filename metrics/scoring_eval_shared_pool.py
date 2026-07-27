#!/usr/bin/env python3
"""
Evaluate sandhi split scoring approaches using Boundary-F1 and Recall@K.

Finds 200 unweighted paths from the graph (K=200 beam), then re-ranks
the same pool using each scoring approach.  This measures how well
each scoring function ranks a large set of candidates, but does NOT
measure how each approach would perform if it drove its own search.

Compares:
  A. Min-words: sort by word count (fewer = better)
  B. CBOW+SP raw: current model.score() (sum of log-probs)
  C. CBOW+SP normalized: model.score() / piece_count
  D. Word-vector: avg piece vecs -> cosine sim between adjacent word vecs
  E. Word-count primary + CBOW tiebreaker (current default)

Usage:
  python metrics/scoring_eval_shared_pool.py --count 200
  python metrics/scoring_eval_shared_pool.py
"""

import logging, os, sys, inspect, time
from collections import defaultdict

import numpy as np
import pandas as pd

from indic_transliteration import sanscript
from sanskrit_parser.base.sanskrit_base import SanskritObject, outputctx
from sanskrit_parser.parser.sandhi_analyzer import LexicalSandhiAnalyzer
from sanskrit_parser.util.lexical_scorer import Scorer, gensim_enabled

BASE_DIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
DATA_DIR = os.path.join(BASE_DIR, '..', 'tests', 'SandhiKosh')
KOSH_FILE = os.path.join(DATA_DIR, 'Result.xls')

logger = logging.getLogger(__name__)


def split_boundaries(words):
    pos = 0
    boundaries = set()
    for w in words:
        pos += len(w)
        boundaries.add(pos)
    boundaries.discard(pos)
    return boundaries


def boundary_f1(candidate_words, reference_words):
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


def score_min_words(path):
    return -len(path)


def score_cbow_raw(paths, scorer):
    sentences = [" ".join(map(str, p)) for p in paths]
    pieces = [scorer.sp.EncodeAsPieces(s) for s in sentences]
    raw = scorer.model.score(pieces, total_sentences=len(sentences))
    return list(raw)


def score_cbow_normalized(paths, scorer):
    sentences = [" ".join(map(str, p)) for p in paths]
    pieces = [scorer.sp.EncodeAsPieces(s) for s in sentences]
    raw = scorer.model.score(pieces, total_sentences=len(sentences))
    return [s / max(len(p), 1) for s, p in zip(raw, pieces)]


def score_wordvec(paths, scorer):
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
    return list(zip([-len(p) for p in paths], cbow_scores))


def evaluate_single(graph, ref_words, scorer, max_k=200):
    """Find up to max_k unweighted paths, then re-rank by each approach."""
    splits = graph.find_all_paths(max_paths=max_k, score=False)
    if not splits:
        return None

    results = {}
    path_strs = [[str(w) for w in p] for p in splits]
    ref_str = list(ref_words)

    # -- Approach A: Min-words --
    scored = [(score_min_words(p), i) for i, p in enumerate(path_strs)]
    scored.sort(key=lambda x: -x[0])
    order = [i for _, i in scored]
    results['min_words'] = _compute_metrics(order, path_strs, ref_str)

    if not gensim_enabled:
        return results

    # -- CBOW scores (shared) --
    cbow_raw = score_cbow_raw(splits, scorer)
    cbow_norm = score_cbow_normalized(splits, scorer)

    # -- Approach B: CBOW raw --
    scored = sorted(enumerate(cbow_raw), key=lambda x: -x[1])
    order = [i for i, _ in scored]
    results['cbow_raw'] = _compute_metrics(order, path_strs, ref_str)

    # -- Approach C: CBOW normalized --
    scored = sorted(enumerate(cbow_norm), key=lambda x: -x[1])
    order = [i for i, _ in scored]
    results['cbow_norm'] = _compute_metrics(order, path_strs, ref_str)

    # -- Approach D: Word-vector --
    wv_scores = score_wordvec(splits, scorer)
    scored = sorted(enumerate(wv_scores), key=lambda x: -x[1])
    order = [i for i, _ in scored]
    results['wordvec'] = _compute_metrics(order, path_strs, ref_str)

    # -- Approach E: Word count primary, CBOW tiebreaker --
    combined = score_wordcount_primary(path_strs, cbow_raw)
    scored = sorted(enumerate(combined), key=lambda x: (-x[1][0], -x[1][1]))
    order = [i for i, _ in scored]
    results['wc_primary'] = _compute_metrics(order, path_strs, ref_str)

    return results


def _compute_metrics(order, path_strs, ref_str):
    n = len(order)
    try:
        pos = order.index(next(i for i, p in enumerate(path_strs) if p == ref_str))
    except (StopIteration, ValueError):
        pos = None

    out = {'n_paths': n, 'pos': pos}
    for k in [1, 5, 10, 50]:
        out[f'recall@{k}'] = 1 if pos is not None and pos < k else 0

    if n > 0:
        best = path_strs[order[0]]
        out['f1_at_1'] = boundary_f1(best, ref_str)
    else:
        out['f1_at_1'] = 0.0

    best_f1 = 0.0
    for rank in range(min(10, n)):
        cand = path_strs[order[rank]]
        f1 = boundary_f1(cand, ref_str)
        best_f1 = max(best_f1, f1)
    out['f1_at_10'] = best_f1

    return out


def load_kosh(count=None):
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


def main(count=None):
    entries = load_kosh(count)
    logger.info("Loaded %d kosh entries", len(entries))

    anal = LexicalSandhiAnalyzer()
    scorer = Scorer() if gensim_enabled else None

    stats = defaultdict(lambda: {
        'count': 0, 'found': 0, 'recall_1': 0, 'recall_5': 0,
        'recall_10': 0, 'recall_50': 0, 'sum_pos': 0,
        'sum_f1_1': 0.0, 'sum_f1_10': 0.0,
    })

    skipped = 0
    start = time.time()

    with outputctx(False):
        for i, ent in enumerate(entries):
            s = SanskritObject(ent['word'], encoding=sanscript.DEVANAGARI,
                               strict_io=True, replace_ending_visarga=None)
            graph = anal.getSandhiSplits(s)
            if graph is None:
                skipped += 1
                continue

            result = evaluate_single(graph, ent['ref'], scorer)
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
                    s['recall_50'] += metrics['recall@50']
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

    print()
    print("=" * 90)
    print(f"{'Approach':<20} {'Recall@1':>9} {'Recall@5':>9} {'Recall@10':>9} "
          f"{'Recall@50':>9} {'F1@1':>7} {'F1@10':>7} {'AvgPos':>7} {'Found':>6}")
    print("-" * 90)
    for approach in ['min_words', 'cbow_raw', 'cbow_norm', 'wordvec', 'wc_primary']:
        if approach not in stats:
            continue
        s = stats[approach]
        c = s['count']
        r1 = s['recall_1'] / c * 100 if c else 0
        r5 = s['recall_5'] / c * 100 if c else 0
        r10 = s['recall_10'] / c * 100 if c else 0
        r50 = s['recall_50'] / c * 100 if c else 0
        f1_1 = s['sum_f1_1'] / c * 100 if c else 0
        f1_10 = s['sum_f1_10'] / c * 100 if c else 0
        avg_pos = s['sum_pos'] / s['found'] if s['found'] else 0
        found_pct = s['found'] / c * 100 if c else 0
        print(f"{approach:<20} {r1:>8.1f}% {r5:>8.1f}% {r10:>8.1f}% "
              f"{r50:>8.1f}% {f1_1:>6.1f}% {f1_10:>6.1f}% "
              f"{avg_pos:>6.1f}  {found_pct:>5.1f}%")
    print("=" * 90)
    print(f"\nSkipped (no graph): {skipped} / {len(entries)}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format="%(levelname)s:%(name)s:%(message)s")
    import argparse
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--count', type=int, default=None,
                   help='Limit to N entries')
    args = p.parse_args()
    main(args.count)
