# sanskrit_parser
Parsers for Sanskrit / संस्कृतम्

[![CI Build Status](https://img.shields.io/travis/kmadathil/sanskrit_parser/master.svg)](https://travis-ci.org/kmadathil/sanskrit_parser)

**NOTE:** This project is still under development. Both over-generation (invalid forms/splits) and under-generation (missing valid forms/splits) are quite likely. Please see the Sanskrit Parser Stack section below for detailed status. Report any issues [here](https://github.com/kmadathil/sanskrit_parser/issues).

Please feel free to ping us if you would like to collaborate on this project.

## Try it out!
- A simple web interface is available at https://sanskrit-parser.appspot.com/
- Launch the [example notebook](https://github.com/kmadathil/sanskrit_parser/blob/master/examples/basic_example.ipynb) on Binder - [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/kmadathil/sanskrit_parser/HEAD?filepath=examples%2Fbasic_example.ipynb)

## Installation

This project has been tested and developed using Python 3.7.

```
pip install sanskrit_parser
```

## Usage
- For a tour of the basic features, check out the [example notebook](https://github.com/kmadathil/sanskrit_parser/blob/master/examples/basic_example.ipynb).
- For more detailed documentation, see [generated sphynx docs](https://kmadathil.github.io/sanskrit_parser/build/html/).
- PS: Command line usage is also documented there.

### Deploying REST API server
Run:
```
sudo mkdir /var/www/.sanskrit_parser
sudo chmod a+rwx /var/www/.sanskrit_parser
```

## Contribution
- Generate docs: `cd docs; make html`


## Sanskrit Parser Stack

Stack of parsing tools

### Level 0
Sandhi splitting subroutine
       Input: Phoneme sequence and Phoneme number to split at
       Action: Perform a sandhi split at given input phoneme number
       Output:  left and right sequences (multiple options will be output).
       No semantic validation will be performed (up to higher levels)

#### Current Status
Module that performs sandhi split/join and convenient rule definition is at `parser/sandhi.py`.

Rule definitions (human readable!) are at `lexical_analyzer/sandhi_rules/*.txt`

This is not accessed standalone from the command line.

### Level 1
* From dhatu + lakAra + puruSha + vachana to pada and vice versa
* From prAtipadika + vibhakti + vachana to pada and vice versa
* Upasarga + dhAtu forms - forward and backwards
* nAmadhAtu forms
* Krt forms  - forwards and backwards
* Taddhita forms  - forwards and backwards

#### Current Status
Bootstrapped using a lexical lookup module built from
1. inriaxmlwrapper + Prof. Gerard Huet's forms database
1. the sanskrit_data project, suitably wrapped

(Either or both of these can be enabled at runtime)

That gives us the minimum we need from Level 1, so Level 2 can work.  As the [generator sub-project](#sanskrit-generator) matures, that will take over the role of this Level

Use `sanskrit_parser tags` on the command line to access this

### Level 2

#### Input
Sanskrit Sentence
#### Action
*   Traverse the sentence, splitting it (or not) at each location to determine all possible valid splits
*   Traverse from left to right
*   Using dynamic programming, assemble the results of all choices

      To split or not to split at each phoneme

      If split, all possible left/right combination of phonemes that can result

      Once split, check if the left section is a valid pada (use level 1 tools to pick pada type and tag morphologically)

      If left section is valid, proceed to split the right section
* At the end of this step, we will have all possible syntactically valid splits with morphological tags

#### Output
All semantically valid sandhi split sequences

#### Current Status
Module at `parser/sandhi_analyer.py`

Use `sanskrit_parser sandhi` on the command line


###    Level 3
#### Input
Semantically valid sequence of tagged padas (output of Level 1)
#### Action:
* Assemble graphs of morphological constraints

    viseShaNa - viseShya

    karaka/vibhakti

    vachana/puruSha constraints on tiGantas and subantas
* Check validity of graphs
#### Output
1.  Is the input sequence a morphologically valid sentence?
1.  Enhanced sequence of tagged padas, with karakas tagged, and a dependency graph associated

#### Current Status
Module at `parser/vakya_analyer.py`

Use `sanskrit_parser vakya` on the command line

## Sanskrit Generator

Generate any valid sanskrit pada using Ashtadhyayi rules, plus vartikas where necessary.

Rules are input in a high level meta-language (currently yaml with imposed semantics - this may change), and the internal rule engine executes rules till a valid pada form is output. Input may be

1. prakriti + pratyaya
1. prakriti + sentence semantics

subantas of ajanta prAtipadikas are currently implemented. Other features are being rolled in.

Use `sanskrit_generator` on the command line

## Seq2Seq based Sanskrit Parser

See: Grammar as a Foreign Language : Vinyals & Kaiser et. al. Google
http://arxiv.org/abs/1412.7449

* Method: Seq2Seq Neural Network (n? layers)
* Input Embedding with word2vec (optional)

### Input
Sanskrit sentence
### Output
Sentence split into padas with tags
### Train/Test data
DCS corpus, converted by Vishvas Vasuki

#### Current Status
Not begun

