---
name: gen-test
description: To run a test or tests for the Sanskrit generator
allowed-tools: Read, Grep, Glob, Bash, Edit, Write
---

# Gen-test Skill

This skill provides instructions for running generator tests in the Sanskrit parser.

## Usage

Use this skill when you need to run tests for the Sanskrit generator component.

## Test Structure

The generator tests are located in `generator/test/` and cover various aspects:

| File | Coverage |
|------|----------|
| `test_ajanta_pum.py` | Ajanta (vowel-final) masculine nominals |
| `test_ajanta_stri.py` | Ajanta feminine nominals |
| `test_ajanta_napum.py` | Ajanta neuter nominals |
| `test_halanta.py` | Halanta (consonant-final) nominals |
| `test_vibhakti.py` | Vibhakti generation across stem classes |
| `test_list.py` / `manual_tests.py` | Regression and manual test cases |

## Running Tests

All tests should be run from the `generator` branch with the virtual environment activated.

### Prerequisites

```bash
source ~/venv/sanskrit/bin/activate
source sourceme
```

### Running All Tests

```bash
pytest -n 8 --dist worksteal sanskrit_parser/generator/test/
```

Be patient and wait for completion. It takes a few minutes

### Running a Specific Test File

```bash
pytest -n 8 --dist worksteal sanskrit_parser/generator/test/test_halanta.py
```
Be patient and wait for completion. It takes a few minutes

### Running Tests for a Specific Pratipadika

```bash
pytest -k "rAma" sanskrit_parser/generator/test/test_ajanta_pum.py
```

### Debugging Failed Tests

When tests fail, use these options for more details:

```bash
pytest --verbose-prakriya --tag-display ...
```

### Generating all vibhakti forms for a pratipadika

```bash
scripts/sanskrit_generator -t rAma --vibhakti
```

### Generating one vibhakti form for a pratipadika

```bash
scripts/sanskrit_generator -t rAma -p su --verbose --tag-display
```

### More options

"""
usage: sanskrit_generator [-h] [--debug] [-p INPUTS [INPUTS ...]] [-d INPUTS]
                          [-t INPUTS] [-m INPUTS [INPUTS ...]]
                          [-u INPUTS [INPUTS ...]] [-s INPUTS [INPUTS ...]]
                          [-o [INPUTS]] [-c [INPUTS]] [-a [INPUTS]]
                          [--vibhakti] [--gen-test] [--prakriya PRAKRIYA]
                          [--sutra-file SUTRA_FILE] [--verbose]
                          [--tag-display]

Paninian Generator: Prakriti + Pratyaya

options:
  -h, --help            show this help message and exit
  --debug
  -p INPUTS [INPUTS ...], --pratyaya INPUTS [INPUTS ...]
  -d INPUTS, --dhatu INPUTS
  -t INPUTS, --pratipadika INPUTS
  -m INPUTS [INPUTS ...], --samasta-pratipadika INPUTS [INPUTS ...]
  -u INPUTS [INPUTS ...], --purva-pada INPUTS [INPUTS ...]
  -s INPUTS [INPUTS ...], --string INPUTS [INPUTS ...]
  -o [INPUTS]           Open bracket
  -c [INPUTS]           Close bracket
  -a [INPUTS]           Avasana
  --vibhakti            generate all vibhaktis
  --gen-test            generate vibhakti test
  --prakriya PRAKRIYA   Prakriya type
  --sutra-file SUTRA_FILE
                        Sutra File Name
  --verbose             verbose
  --tag-display         display tags and its on objects (requires --verbose)
  """

