# Developer Guide

A guide for contributors and new developers on the Sanskrit Parser codebase.

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Dev Environment Setup](#dev-environment-setup)
3. [Repository Layout](#repository-layout)
4. [Architecture Overview](#architecture-overview)
5. [Key Classes](#key-classes)
6. [Data Flow Walkthrough](#data-flow-walkthrough)
7. [Encoding and Transliteration](#encoding-and-transliteration)
8. [Running Tests](#running-tests)
9. [Adding Features](#adding-features)
10. [Generator](#generator)
11. [Generating Docs](#generating-docs)

---

## Prerequisites

**Python:** 3.11 (preferred)

**Helpful background:**
- Basic familiarity with Sanskrit linguistics is useful but not required
- **Sandhi** is the system of phonological rules that govern how sounds combine at word boundaries in Sanskrit. For example, `asti + uttarasyAm` → `astyuttarasyAm`. The parser reverses this process.
- **Pada** means a grammatical word form. A pada carries morphological tags (case, number, gender for nominals; tense, person, number for verbs).
- **Vibhakti** = grammatical case. **Vachana** = number (singular/dual/plural). **Linga** = gender.

---

## Dev Environment Setup

```bash
# Clone the repo
git clone git@github.com:kmadathil/sanskrit_parser.git
cd sanskrit_parser

# Install in editable mode with dev and test dependencies
pip install -e .[dev,test]

# Optional: statistical scoring (requires a C compiler)
pip install gensim sentencepiece
```

The package registers two CLI entry points: `sanskrit_parser` and `sanskrit_generator`.

---

## Repository Layout

```
sanskrit_parser/
├── api.py                      # Main Parser class — primary public API
├── cmd_line.py                 # CLI entry point
│
├── base/
│   ├── sanskrit_base.py        # SanskritString, SanskritObject, SanskritNormalizedString
│   └── maheshvara_sutra.py     # Maheshvara sutra phoneme groupings
│
├── parser/
│   ├── sandhi.py               # Low-level sandhi split/join rules (Level 0)
│   ├── sandhi_analyzer.py      # LexicalSandhiAnalyzer — DP-based sentence splitting (Level 2)
│   ├── datastructures.py       # SandhiGraph, VakyaGraph, VakyaParse (core DAG structures)
│   └── vakya_analyzer.py       # Morpho-syntactic analysis (Level 3)
│
├── generator/
│   ├── generator.py            # Sanskrit word generator (Ashtadhyayi rules)
│   ├── maheshvara.py           # Maheshvara sutra implementation
│   ├── sutra.py                # Paninian rule definitions
│   ├── pratyaya.py             # Suffix handling
│   ├── operations.py           # Phonological operations
│   └── dhatu.py                # Root verb management
│
├── util/
│   ├── lexical_lookup.py       # Abstract base class for lexical lookup
│   ├── lexical_lookup_factory.py # CombinedWrapper + factory
│   ├── inriaxmlwrapper.py      # Inria XML database backend
│   ├── sanskrit_data_wrapper.py # Sanskrit Data project backend
│   ├── DhatuWrapper.py         # Root verb (dhatu) lookup
│   ├── lexical_scorer.py       # Gensim/sentencepiece statistical scorer
│   └── disjoint_set.py         # Union-Find data structure
│
└── rest_api/
    └── api_v1.py               # Flask REST endpoints

tests/                          # pytest test suite (20 files)
data/                           # Sanskrit databases and ML models
examples/                       # Jupyter notebooks
docs/                           # Sphinx documentation source
```

---

## Architecture Overview

Parsing is organized into four levels:

```
Input Sanskrit text
        │
        ▼
┌───────────────────────────────┐
│  Level 0: Sandhi              │  sandhi.py
│  Split phoneme sequences      │  Rules in lexical_analyzer/sandhi_rules/*.txt
└───────────────┬───────────────┘
                │
                ▼
┌───────────────────────────────┐
│  Level 1: Morphological Tags  │  inriaxmlwrapper.py
│  Look up valid pada forms     │  sanskrit_data_wrapper.py
│  and their grammatical tags   │
└───────────────┬───────────────┘
                │
                ▼
┌───────────────────────────────┐
│  Level 2: Sandhi Analysis     │  sandhi_analyzer.py
│  DP traversal to find all     │  datastructures.py (SandhiGraph)
│  valid word segmentations     │
└───────────────┬───────────────┘
                │
                ▼
┌───────────────────────────────┐
│  Level 3: Vakya Analysis      │  vakya_analyzer.py
│  Dependency graph, karaka     │  datastructures.py (VakyaGraph)
│  assignment, syntax checking  │
└───────────────────────────────┘
```

The key insight is that each level's output feeds the next. The system does not commit to a single parse path early — it uses a DAG to represent all possible interpretations simultaneously, then prunes.

---

## Key Classes

### `Parser` — `sanskrit_parser/api.py`

The top-level entry point for all parsing. Users should interact with this class rather than lower-level modules.

```python
from sanskrit_parser import Parser
parser = Parser(input_encoding='SLP1', output_encoding='SLP1')

# Get sandhi splits
for split in parser.split("astyuttarasyAMdiSi", limit=10):
    print(split)

# Get full morpho-syntactic parses
for split in parser.split("astyuttarasyAMdiSi", limit=10):
    for parse in split.parse(limit=5):
        print(parse)
```

Key constructor parameters:
- `input_encoding` / `output_encoding` — transliteration scheme (SLP1, IAST, DEVANAGARI, etc.)
- `lexical_lookup` — `"combined"` (default), `"inria"`, or `"sanskrit_data"`
- `replace_ending_visarga` — set to `'s'` if visarga at sentence end should be treated as `s`

### `LexicalSandhiAnalyzer` — `sanskrit_parser/parser/sandhi_analyzer.py`

Implements the Level 2 DP traversal. Given a Sanskrit sentence as a `SanskritObject`, it:
1. Iterates through every position in the string
2. Calls `Sandhi.split_at()` to get all phonologically valid splits at each position
3. Checks via lexical wrappers whether the left segment is a valid pada
4. Builds a `SandhiGraph` DAG from valid left segments

```python
analyzer = LexicalSandhiAnalyzer()
graph = analyzer.getSandhiSplits(SanskritObject("astyuttarasyAMdiSi"))
splits = graph.findAllPaths(10)
```

### `SandhiGraph` — `sanskrit_parser/parser/datastructures.py`

A directed acyclic graph where:
- **Nodes** are `SanskritObject` instances (candidate word forms)
- **Edges** represent valid "follows" relationships between adjacent words
- `__start__` and `__end__` sentinel nodes bound the graph
- `findAllPaths()` traverses the DAG to enumerate complete sentences

### `VakyaGraph` — `sanskrit_parser/parser/datastructures.py`

Builds on a `SandhiGraph` path (a list of tagged padas) to construct a dependency graph for Level 3 analysis. Nodes are `VakyaGraphNode` instances carrying morphological tags; edges represent syntactic relationships (karaka, viseshana, etc.).

### `Sandhi` — `sanskrit_parser/parser/sandhi.py`

Low-level sandhi rule engine. Maintains forward (join) and backward (split) rule tables loaded from text files.

```python
sandhi = Sandhi()
# All possible splits of "astyuttara" at position 4:
splits = sandhi.split_at(word, idx=4)
```

The `Sandhi` singleton is shared across all `LexicalSandhiAnalyzer` instances.

### Lexical Wrappers — `sanskrit_parser/util/`

Two backends, both implementing the `LexicalLookup` interface (`lexical_lookup.py`):

| Class | Backend | File |
|---|---|---|
| `InriaXMLWrapper` | Prof. Gérard Huet's morphological database (SQLite) | `inriaxmlwrapper.py` |
| `SanskritDataWrapper` | Sanskrit Data project | `sanskrit_data_wrapper.py` |
| `CombinedWrapper` | Merges both backends | `lexical_lookup_factory.py` |

All three expose the same interface:
```python
wrapper.valid(word)           # bool — is this a valid pada?
wrapper.get_tags(word)        # list of (stem, tagset) tuples
```

---

## Data Flow Walkthrough

Here is what happens when you call `parser.split("astyuttarasyAMdiSi")`:

1. **Input normalization** (`sanskrit_base.py`)
   The input string is wrapped in a `SanskritNormalizedString`. If the encoding is not SLP1, it is transliterated to SLP1 internally using `indic_transliteration`.

2. **Sandhi graph construction** (`sandhi_analyzer.py: getSandhiSplits()`)
   The analyzer iterates left-to-right across every character position `i` in the string:
   - Calls `sandhi.split_at(word, i)` to get all phonologically possible `(left, right)` splits
   - Checks if `left` is a valid pada using the lexical wrapper
   - If valid, adds `left` as a node in the `SandhiGraph` with an edge from the appropriate predecessor

3. **Path enumeration** (`datastructures.py: SandhiGraph.findAllPaths()`)
   Traverses the DAG from `__start__` to `__end__` to enumerate all complete sentence segmentations. Paths are scored (if a scorer is available) and returned ranked.

4. **Morphological tagging**
   Each word in a path is looked up via `getMorphologicalTags()` to retrieve all possible `(stem, tagset)` pairs.

5. **Vakya analysis** (`datastructures.py: VakyaGraph`)
   For Level 3 parses, a `VakyaGraph` is built from each tagged split. It applies constraint rules (agreement in case/number/gender, karaka assignment) to check syntactic validity and produce dependency structure.

---

## Encoding and Transliteration

**Internal representation is always SLP1** — a compact ASCII encoding for Sanskrit.

The `indic_transliteration` library handles conversion between:
- `SLP1` (internal)
- `IAST` (International Alphabet of Sanskrit Transliteration, e.g. `ā ī ū`)
- `DEVANAGARI` (e.g. `अ आ इ`)
- `HK` (Harvard-Kyoto), `VELTHUIS`, `WX`, and others

Key classes in `base/sanskrit_base.py`:

| Class | Description |
|---|---|
| `SanskritString` | Base class; stores string in SLP1 internally |
| `SanskritImmutableString` | Hashable; used as dict keys and graph nodes |
| `SanskritNormalizedString` | Applies normalization (anusvara, visarga) on top of SLP1 |
| `SanskritObject` | Full object with morphological tag support |

When writing code that constructs Sanskrit strings, always use these classes rather than raw Python strings. This ensures encoding consistency throughout the pipeline.

---

## Running Tests

```bash
# Run the main test suites
pytest tests/test_sandhi.py tests/test_parser.py --test-count 1000

# Run a specific test file
pytest tests/test_SanskritLexicalAnalyzer.py -v

# Run the full matrix across Python versions (requires tox)
tox

# Quick smoke test during development (fewer iterations)
pytest tests/test_parser.py --test-count 10
```

Key test files and what they cover:

| File | What it tests |
|---|---|
| `test_sandhi.py` | Sandhi split and join rule correctness |
| `test_parser.py` | End-to-end parse of known sentences |
| `test_SanskritLexicalAnalyzer.py` | Lexical lookup and morphological tagging |
| `test_DhatuWrapper.py` | Root verb (dhatu) database lookups |
| `test_SandhiKosh.py` | Sandhi rule database integrity |

The `--test-count` flag controls how many test sentences are exercised. CI runs with 1000; use a lower value (10–50) for fast local iteration.

---

## Adding Features

### Adding new sandhi rules

Rules live in plain text files under `sanskrit_parser/lexical_analyzer/sandhi_rules/`. Each file covers a category of rules (vowel sandhi, consonant sandhi, etc.). The format is human-readable; see existing files for examples. After editing, run `test_sandhi.py` to validate.

### Adding a new lexical backend

1. Subclass `LexicalLookup` in `sanskrit_parser/util/lexical_lookup.py`
2. Implement `valid(word) -> bool` and `get_tags(word, tmap=True) -> list`
3. Register it in `LexicalLookupFactory.create()` in `lexical_lookup_factory.py`

### Extending morpho-syntactic analysis (Level 3)

The constraint rules that govern dependency graph construction are in `datastructures.py` in the `VakyaGraph` class. New karaka or agreement rules can be added there.

### Adding generator rules

The generator lives on the `generator` branch. See [Generator.md](Generator.md) for a full description of the architecture, the YAML rule DSL, and how to add new sutras.

---

## Generator

The generator (`sanskrit_parser/generator/`) derives Sanskrit word forms from roots and stems by applying Paninian (Ashtadhyayi) grammar rules. It is developed on the `generator` branch (not merged to master).

For full documentation — module structure, the prakriya engine, sutra YAML DSL, rule priority, and worked examples — see **[Generator.md](Generator.md)**.

---

## Generating Docs

The project uses Sphinx with reStructuredText sources in `docs/`.

```bash
cd docs
make html
# Output is in docs/build/html/index.html
```

The hosted docs are at https://kmadathil.github.io/sanskrit_parser/build/html/.
