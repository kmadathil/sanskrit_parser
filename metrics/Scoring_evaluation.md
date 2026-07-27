# Scoring Evaluation — Sandhi Split Ranking

Two evaluation harnesses measure how well different scoring approaches
rank sandhi split candidates from the DAG.

---

## Test A: Shared 200-Path Pool (Reranking Only)

**File:** `scoring_eval_shared_pool.py`

**Setup:** Find 200 paths from the graph using unit-weight (unweighted)
search with beam K=200.  All five approaches re-rank the identical pool.
This measures scoring power in isolation — how well each approach
identifies the correct split when given a large, diverse pool of
candidates — but does NOT measure how each approach performs when it
drives its own search.

**Results (all 9042 sandhi kosha entries):**

```
==============================================================================
Approach              Recall@1  Recall@5 Recall@10 Recall@50    F1@1   F1@10  AvgPos  Found
------------------------------------------------------------------------------
min_words                57.8%     92.8%     97.0%     99.6%   73.7%   99.5%    1.6  100.0%
cbow_raw                 67.2%     91.6%     97.4%    100.0%   85.2%   99.6%    1.3  100.0%
cbow_norm                32.8%     54.8%     64.6%     84.4%   61.4%   89.0%   23.1  100.0%
wordvec                   7.2%     18.2%     27.0%     52.2%   37.0%   64.7%   71.8  100.0%
wc_primary               73.4%     98.0%     99.4%    100.0%   81.8%  100.0%    0.5  100.0%
==============================================================================
```

**Key observations:**
- All approaches have 100% Found — the unweighted K=200 beam captures
  the correct split for every entry.
- `wc_primary` (word-count-first + CBOW tiebreaker) wins on Recall@1
  (73.4%) and Recall@5 (98.0%).
- `cbow_raw` does well on Recall@1 (67.2%) but the tiebreaker in
  `wc_primary` adds 6 points.
- `cbow_norm` performs poorly — normalizing by piece count destroys the
  signal.
- `wordvec` is not useful as a standalone scorer (7.2% Recall@1).
- This evaluation **overestimates** performance because it gives every
  approach a large, pre-computed pool that is not representative of what
  each approach would find under its own search.

---

## Test B: Per-Approach DAG Search (Honest)

**File:** `scoring_eval.py`

**Setup:** Each approach drives its own DAG search with beam K=10
(corresponding to production `max_paths`).  Weighted approaches
(`cbow_raw`, `cbow_norm`) set per-edge weights matching `score_graph()`
(bigrams for internal edges) and run weighted shortest-path search.
Unweighted approaches use unit-weight search.  `wc_primary` re-ranks
the unweighted search pool with word-count-first + CBOW tiebreaker.
`wordvec` is evaluated only as a re-ranker on the unweighted pool (it
cannot be expressed as independent per-edge weights).

**Results (all 9042 sandhi kosha entries):**

```
==============================================================================
Approach              Recall@1  Recall@5 Recall@10    F1@1   F1@10  AvgPos  Found
------------------------------------------------------------------------------
min_words                66.0%     94.1%     97.5%   81.3%   99.4%    0.7   97.5%
cbow_raw                 77.9%     95.4%     97.8%   88.3%   99.4%    0.5   97.8%
cbow_norm                57.0%     89.7%     95.3%   74.8%   98.9%    1.0   95.3%
wordvec                  12.5%     44.3%     97.5%   46.8%   99.4%    4.8   97.5%
wc_primary               83.7%     97.2%     97.5%   89.5%   99.4%    0.2   97.5%
==============================================================================
```

**Key observations:**
- Found drops to ~97.5% for unweighted approaches — 2.5% of correct
  splits have more words than the 10 shortest paths found (a fundamental
  limitation of word-count-first search at K=10).
- `wc_primary` wins on Recall@1 (83.7%) — the CBOW tiebreaker
  effectively selects the best among shortest paths.
- `cbow_raw` with bigram edge weights scores 77.9% Recall@1 and
  achieves the highest Found (97.8%), capturing 0.3% more entries than
  unweighted search.  However, its weighted beam sometimes drops the
  correct split (91.3% Found before the bigram fix → 97.8% after).
- `wc_primary` and `cbow_raw` are complementary: `wc_primary` is better
  at ranking the correct split #1 when it's in the shortest-path pool;
  `cbow_raw` finds correct splits slightly more often (97.8% vs 97.5%)
  but ranks them lower.
- `min_words` (no CBOW tiebreaker) drops 17.7 points from `wc_primary`,
  confirming the tiebreaker is essential.
- `cbow_norm` trails `cbow_raw` across the board.
- `wordvec` remains unusable as a standalone scorer (12.5% Recall@1).

---

## Test C: Per-Approach DAG Search, K=50

**Setup:** Same as Test B, but with beam K=50 (`--max-paths 50`).
This is a production-tunable knob — wider beam captures more candidates
at the cost of slower search.

**Results (all 9042 sandhi kosha entries):**

```
==============================================================================
Approach              Recall@1  Recall@5 Recall@10    F1@1   F1@10  AvgPos  Found
------------------------------------------------------------------------------
min_words                65.8%     94.1%     97.4%   81.2%   99.7%    1.1   99.7%
cbow_raw                 77.9%     95.4%     97.8%   88.3%   99.4%    0.7   99.5%
cbow_norm                57.0%     89.7%     95.3%   74.8%   98.9%    1.7   99.4%
wordvec                   8.3%     24.9%     37.0%   39.5%   74.3%   21.4   99.7%
wc_primary               84.3%     98.8%     99.5%   89.7%   99.9%    0.3   99.7%
==============================================================================
```

**Key observations:**
- Found rises to 99.7% (was 97.5% at K=10) — only ~25 of 9042 entries
  miss the correct split entirely.
- `wc_primary` R@1 improves from 83.7% → 84.3% with the wider beam.
- `cbow_raw` R@1 stays flat at 77.9% — its weighted beam converges
  faster and doesn't benefit from the wider K.
- The 0.3% missed entries likely have the correct split at position
  51+ (more words than the 50 shortest splits).

### Test C.1: Per-Approach DAG Search, K=20
```
==============================================================================
Approach              Recall@1  Recall@5 Recall@10    F1@1   F1@10  AvgPos  Found
------------------------------------------------------------------------------
min_words                65.4%     93.8%     97.3%   80.5%   99.5%    0.9   98.9%
cbow_raw                 77.9%     95.4%     97.8%   88.3%   99.4%    0.6   99.0%
cbow_norm                57.0%     89.7%     95.3%   74.8%   98.9%    1.3   98.1%
wordvec                   9.6%     30.1%     48.6%   42.6%   83.4%    9.6   98.9%
wc_primary               84.1%     98.5%     98.9%   89.7%   99.7%    0.2   98.9%
==============================================================================
```
---

## Comparison: All Tests

| Metric | Test A (shared K=200) | Test B (K=10) | Test C (K=50) |
|---|---|---|---|
| Search | Unweighted shared pool | Per-approach | Per-approach |
| Found | 100% | 97.5% | 99.7% |
| wc_primary R@1 | 73.4% | 83.7% | **84.3%** |
| wc_primary R@5 | 98.0% | 97.2% | **98.8%** |
| wc_primary R@10 | 99.4% | 97.5% | **99.5%** |
| cbow_raw R@1 | 67.2% | 77.9% | **77.9%** |
| cbow_raw R@5 | 91.6% | 95.4% | **95.4%** |

Test C (K=50 per-approach) is the recommended evaluation mode: it
combines the honesty of per-approach search with Found close to 100%.
The `--max-paths` / `-k` flag in `scoring_eval.py` makes it easy to
tune the beam for production trade-offs.

---

## Edge Weight Design

`score_graph()` (in `sanskrit_parser/parser/datastructures.py`) sets
edge weights as:

- `start → w`: score single word `[w]`
- `w → end`: score single word `[w]`
- `w1 → w2`: score bigram `str(w1) + " " + str(w2)` (two-word sentence)

All scores are negated for search (lower weight = better path).
This bigram weighting is critical — early experiments with unigram
(destination-only) edge weights gave Found of only 91.3% for
`cbow_raw`, compared to 97.8% with the correct bigram scheme.
