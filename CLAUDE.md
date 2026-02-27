# CLAUDE.md

## Project Overview

Sanskrit Parser is a Python library for morphological and syntactic analysis of Sanskrit text. It provides three levels of parsing:

- **Level 1 (Tags)**: Morphological analysis of individual words
- **Level 2 (Sandhi)**: Sentence segmentation via sandhi splitting
- **Level 3 (Vakya)**: Full morpho-syntactic analysis with dependency graphs

## Commands

```bash
# Install for development
pip install -e .

# Run tests
pytest --test-count 1000 tests/test_DhatuWrapper.py tests/test_sandhi.py tests/test_SanskritLexicalAnalyzer.py tests/test_SandhiKosh.py tests/test_parser.py
tox  # across Python versions

# Lint
flake8  # max line length 150 (see setup.cfg)

# CLI usage
sanskrit_parser vakya <sentence>
sanskrit_parser tags <word>
sanskrit_parser sandhi <sentence>
```

## Architecture

### Entry Points
- `sanskrit_parser/api.py` - Main `Parser` class (primary user-facing API)
- `sanskrit_parser/cmd_line.py` - CLI interface (`sanskrit_parser.cmd_line:cmd_line`)
- `sanskrit_parser/rest_api/api_v1.py` - Flask-RESTX REST endpoints (port 9000)

### Core Modules
- `parser/sandhi.py` - Sandhi split/join rules
- `parser/sandhi_analyzer.py` - Lexical sandhi analysis; LRU cache (256 entries) on `_is_valid_word()`
- `parser/datastructures.py` - DAG structures for sandhi and vakya graphs (~58KB); **debug logging is disabled here — do not re-enable (causes 80+ calls per parse)**

### Lexical Lookup
- `util/lexical_lookup.py` - Abstract base
- `util/lexical_lookup_factory.py` - `CombinedWrapper` factory (merges Inria + Sanskrit Data)
- `util/inriaxmlwrapper.py` - Inria XML database
- `util/sanskrit_data_wrapper.py` - Sanskrit Data project
- `util/lexical_scorer.py` - Gensim-based statistical scoring

### Generator
- `generator/generator.py` - Main generation engine
- Implements Ashtadhyayi (Paninian grammar) rules via YAML sutra definitions

## Key Design Decisions

### Performance (Critical)
Preserve these optimizations:
- LRU caching (`@lru_cache(256)`) in `sandhi_analyzer.py` on `_is_valid_word()`
- `node_cache` dict in `sandhi_analyzer.py` to reuse `SanskritObject` instances during DAG construction
- `CombinedWrapper` is cached — do not create new instances per parse
- `fast_merge=True` (default) in `Parser` and `VakyaGraph` for optimized merge strategy
- Divide-and-conquer parsing in `VakyaGraph` controlled by `max_parse_dc` (default: 4) and `split_above` (default: 5) in `Parser`
- Debug logging in `parser/datastructures.py` must remain disabled

### Layered DAG Architecture
Parsing builds directed acyclic graphs representing all possible sandhi splits, then applies divide-and-conquer DP traversal to find valid morphological analyses. Avoid approaches that require backtracking.

### Transliteration
Uses `indic_transliteration` library. Internal representation is typically SLP1. API accepts/returns configurable encodings (SLP1, IAST, Devanagari, etc.).

## Dependencies

**Required:** `indic_transliteration`, `lxml`, `networkx`, `tinydb`, `six`, `flask`, `flask_restx`, `flask_cors`, `jsonpickle`, `sanskrit_util`, `sqlalchemy>=1.4`, `pydot`, `pandas`, `xlrd`, `importlib_resources`, `werkzeug==2.1.2`

**Optional:** `gensim`, `sentencepiece` (statistical scoring — needed for App Engine deployment)

## Data Files

- `data/sanskrit_data.db` - SQLite word forms database (17MB)
- `data/sentencepiece.model` - SentencePiece tokenization model
- `data/word2vec_model.dat` - Word2Vec embeddings (7.8MB)
- `data/dhAtu-pATha-kRShNAchArya.json` - Root verb database
- `parser/sandhi_rules/*.txt` - Compiled sandhi rules (included as package data)

## Active Branches

### `perf` branch
Contains performance work (71.6x speedup: 1800ms → 25ms) not yet merged to master. Includes LRU caching, beam search/early pruning, disabled debug logging, and CombinedWrapper caching. **Any changes touching the parser pipeline must be tested against this branch** — run the full pytest suite and verify parse times stay under 100ms.

### `generator` branch
The generator module (`sanskrit_parser/generator/`) lives here and is not yet merged to master. All generator development (Ashtadhyayi/Paninian rule implementation, sutra additions) should happen on this branch.

## CI/CD

GitHub Actions (`.github/workflows/build_and_test.yml`): Ubuntu latest, Python 3.11 only. On push/PR to master: builds wheel, then runs pytest with 1000 iterations. Flake8 linting is currently disabled in CI. App Engine deployment via `app_engine.yml` on release.

## Testing Notes

- Tests use `--test-count` flag to control iteration count
- Key test files: `test_sandhi.py`, `test_parser.py`, `test_SanskritLexicalAnalyzer.py`, `test_DhatuWrapper.py`, `test_SandhiKosh.py`
- Additional tests: `tests/parser/test_conll.py` (CoNLL format), `test_rest_api.py`
- Performance regression tests exist — verify parse times stay reasonable
