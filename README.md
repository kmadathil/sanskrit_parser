# sanskrit_parser
Parsers for Sanskrit / संस्कृतम्

**NOTE:** This project is still under development. Both over-generation (invalid forms/splits) and under-generation (missing valid forms/splits) are quite likely. Please see the Sanskrit Parser Stack section below for detailed status. Report any issues [here](https://github.com/kmadathil/sanskrit_parser/issues).

Please feel free to ping us if you would like to collaborate on this project.

## Installation

This project has been tested and developed using Python 2.7. A port to Python 3 has been completed, and everything *should* now work in both versions of Python. 
```
pip install sanskrit_parser
```

## Usage

### Lexical Analyzer
Use the `SanskritLexicalAnalyzer` to split a sentence (wrapped in a `SanskritObject`) and retrieve the top 10 splits:
```python
>>> from sanskrit_parser.lexical_analyzer.SanskritLexicalAnalyzer import SanskritLexicalAnalyzer
>>> from sanskrit_parser.base.SanskritBase import SanskritObject, SLP1
>>> sentence = SanskritObject("astyuttarasyAMdishidevatAtmA")
>>> analyzer = SanskritLexicalAnalyzer()
>>> splits = analyzer.getSandhiSplits(sentence).findAllPaths(10)
>>> for split in splits:
...    print split
...
[u'asti', u'uttarasyAm', u'diSi', u'devatA', u'AtmA']
[u'asti', u'uttarasyAm', u'diSi', u'devat', u'AtmA']
[u'asti', u'uttarasyAm', u'diSi', u'devata', u'AtmA']
[u'asti', u'uttara', u'syAm', u'diSi', u'devatA', u'AtmA']
[u'asti', u'uttarasyAm', u'diSi', u'devatA', u'at', u'mA']
[u'asti', u'uttarasyAm', u'diSi', u'de', u'vatA', u'AtmA']
[u'asti', u'uttarasyAm', u'diSi', u'devata', u'at', u'mA']
[u'asti', u'uttas', u'rasyAm', u'diSi', u'devat', u'AtmA']
[u'asti', u'uttara', u'syAm', u'diSi', u'devat', u'AtmA']
[u'asti', u'uttarasyAm', u'diSi', u'de', u'avatA', u'AtmA']
```

The lexical_analyzer can also be used to look up the tags for a given word form in the INRIA database:<br>
(Note that the database stores words ending in visarga with an 's' at the end)
```python
>>> word = SanskritObject('hares')
>>> tags = analyzer.getLexicalTags(word)
>>> for tag in tags:
...    print tag
...
('hf#1', set(['cj', 'snd', 'prim', 'para', 'md', 'sys', 'prs', 'v', 'np', 'sg', 'op']))
('hari#1', set(['na', 'mas', 'sg', 'gen']))
('hari#1', set(['na', 'mas', 'abl', 'sg']))
('hari#1', set(['na', 'fem', 'sg', 'gen']))
('hari#1', set(['na', 'fem', 'abl', 'sg']))
('hari#2', set(['na', 'mas', 'sg', 'gen']))
('hari#2', set(['na', 'mas', 'abl', 'sg']))
('hari#2', set(['na', 'fem', 'sg', 'gen']))
('hari#2', set(['na', 'fem', 'abl', 'sg']))
```

### Morphological Analyzer

The `SanskritMorphologicalAnalyzer` class has a similar interface to `SanskritLexicalAnalyzer`, and has a `constrainPath()` method which can find whether a particular split has a valid morphology, and output all such valid morphologies.
```python
>>> from sanskrit_parser.base.SanskritBase import SanskritObject, SLP1
>>> from sanskrit_parser.morphological_analyzer.SanskritMorphologicalAnalyzer import SanskritMorphologicalAnalyzer
>>> sentence = SanskritObject("astyuttarasyAm")
>>> analyzer = SanskritMorphologicalAnalyzer()
>>> graph=analyzer.getSandhiSplits(sentence,tag=True)
>>> splits=graph.findAllPaths()
>>> for sp in splits:
>>>     print("Lexical Split:",sp)
>>>     p=analyzer.constrainPath(sp)
>>>     if p:
>>>         print("Valid Morphologies")
>>>         for pp in p:
>>>             print([(spp,pp[str(spp)]) for spp in sp])
>>>     else:
>>>         print("No valid morphologies for this split")
...
('Lexical Split:', [asti, uttarasyAm])
Valid Morphologies
[(asti, ('as#1', set([kartari, law, ekavacanam, prATamikaH, praTamapuruzaH]))), (uttarasyAm, ('uttara#2', set([strIliNgam, saptamIviBaktiH, ekavacanam])))]
[(asti, ('as#1', set([kartari, law, ekavacanam, prATamikaH, praTamapuruzaH]))), (uttarasyAm, ('uttara#1', set([strIliNgam, saptamIviBaktiH, ekavacanam])))]
('Lexical Split:', [asti, uttara, syAm])
No valid morphologies for this split
('Lexical Split:', [asti, ut, tara, syAm])
No valid morphologies for this split
```

### InriaXMLWrapper

The InriaXMLWrapper utility class can also be used to lookup tags:
```python
>>> from sanskrit_parser.util.inriaxmlwrapper import InriaXMLWrapper
>>> db = InriaXMLWrapper()
>>> db_tags = db.get_tags('hares')
>>> tags == db_tags
True
```

### Sandhi

The `Sandhi` class can be used to join/split words:
```python
>>> from sanskrit_parser.lexical_analyzer.sandhi import Sandhi
>>> sandhi = Sandhi()
>>> word1 = SanskritObject('te')
>>> word2 = SanskritObject('eva')
>>> joins = sandhi.join(word1, word2)
>>> for join in joins:
...    print join
...
teeva
taeva
ta eva
tayeva
```

To split at a specific position, use the `Sandhi.split_at()` method:
```python
>>> w = SanskritObject('taeva')
>>> splits = sandhi.split_at(w, 1)
>>> for split in splits:
...    print split
...
(u'tar', u'eva')
(u'tas', u'eva')
(u'taH', u'eva')
(u'ta', u'eva')
```

To split at all possible locations, use the `Sandhi.split_all()` method:
```python
>>> splits_all = sandhi.split_all(w)
>>> for split in splits_all:
...    print split
...
(u't', u'aeva')
(u'tar', u'eva')
(u'taev', u'a')
(u'to', u'eva')
(u'ta', u'eva')
(u'te', u'eva')
(u'taH', u'eva')
(u'tae', u'va')
(u'taeva', u'')
(u'tas', u'eva')
```

**Note**: As mentioned previously, both over-generation and under-generation are possible with the `Sandhi` class.

### MaheshvaraSutras
Get varnas in a pratyahara:
```python
>>> from sanskrit_parser.base.MaheshvaraSutras import MaheshvaraSutras
>>> MS = MaheshvaraSutras()
>>> jaS = SanskritObject('jaS', encoding=SLP1)
>>> print MS.getPratyahara(jaS)
jabagaqada
```
Check if a varna is in a pratyahara:
```python
>>> g = SanskritObject('g')
>>> print MS.isInPratyahara(jaS, g)
True
>>> k = SanskritObject('k')
>>> print MS.isInPratyahara(jaS, k)
False
```

### SanskritObject
`SanskritObject` is a base class used in all modules. It supports automatic detection of input encoding and transcoding to any encoding supported by the `indic_transliteration` package.
```python
>>> from sanskrit_parser.base.SanskritBase import SanskritObject, SLP1
>>> sentence = SanskritObject("astyuttarasyAMdishidevatAtmA")
>>> print sentence.transcoded(SLP1)
astyuttarasyAMdiSidevatAtmA
```


### Command Line Usage
All the classes described above can also be used from the command line. The corresponding examples are below. Please run the tools with `--help/-h` to get help on the options


#### SanskritMorphologicalAnalyzer
```
$ python -m sanskrit_parser.morphological_analyzer.SanskritMorphologicalAnalyzer astyuttarasyAm --input-encoding SLP1 --need-lakara
Input String: astyuttarasyAm
Input String in SLP1: astyuttarasyAm
Start Split: 2017-10-01 11:16:10.489660
End DAG generation: 2017-10-01 11:16:10.496199
End pathfinding: 2017-10-01 11:16:10.497342
Splits:
Lexical Split: [asti, uttarasyAm]
Valid Morphologies
[(asti, ('as#1', set([kartari, law, ekavacanam, prATamikaH, praTamapuruzaH]))), (uttarasyAm, ('uttara#2', set([strIliNgam, saptamIviBaktiH, ekavacanam])))]
[(asti, ('as#1', set([kartari, law, ekavacanam, prATamikaH, praTamapuruzaH]))), (uttarasyAm, ('uttara#1', set([strIliNgam, saptamIviBaktiH, ekavacanam])))]
Lexical Split: [asti, uttara, syAm]
No valid morphologies for this split
Lexical Split: [asti, ut, tara, syAm]
No valid morphologies for this split
```

#### SanskritLexicalAnalyzer
```
$ python -m sanskrit_parser.lexical_analyzer.SanskritLexicalAnalyzer astyuttarasyAMdishidevatAtmA --split
Splits:
[u'asti', u'uttarasyAm', u'diSi', u'devat', u'AtmA']
[u'asti', u'uttarasyAm', u'diSi', u'devata', u'AtmA']
[u'asti', u'uttarasyAm', u'diSi', u'devatA', u'AtmA']
[u'asti', u'uttara', u'syAm', u'diSi', u'devat', u'AtmA']
[u'asti', u'uttarasyAm', u'diSi', u'devata', u'at', u'mA']
[u'asti', u'uttarasyAm', u'diSi', u'de', u'vatAt', u'mA']
[u'asti', u'uttarasyAm', u'diSi', u'devatA', u'at', u'mA']
[u'asti', u'uttas', u'asyAm', u'diSi', u'devat', u'AtmA']
[u'asti', u'uttara', u'syAm', u'diSi', u'devata', u'AtmA']
[u'asti', u'uttarasyAm', u'diSi', u'de', u'vatA', u'AtmA']

$ python -m sanskrit_parser.lexical_analyzer.SanskritLexicalAnalyzer hares
Input String: hares
Input String in SLP1: hares
[('hf#1', set(['cj', 'snd', 'prim', 'para', 'md', 'sys', 'prs', 'v', 'np', 'sg', 'op'])), ('hari#1', set(['na', 'mas', 'sg', 'gen'])), ('hari#1', set(['na', 'mas', 'abl', 'sg'])), ('hari#1', set(['na', 'fem', 'sg', 'gen'])), ('hari#1', set(['na', 'fem', 'abl', 'sg'])), ('hari#2', set(['na', 'mas', 'sg', 'gen'])), ('hari#2', set(['na', 'mas', 'abl', 'sg'])), ('hari#2', set(['na', 'fem', 'sg', 'gen'])), ('hari#2', set(['na', 'fem', 'abl', 'sg']))]
```



#### InriaXMLWrapper
```
$ python -m sanskrit_parser.util.inriaxmlwrapper hares
INFO:root:Pickle file found, loading at 2017-07-31 14:35:56.093000
INFO:root:Loading finished at 2017-07-31 14:35:59.159000, took 3.066000 s
INFO:root:Cached 666994 forms for fast lookup
Getting tags for hares
('hf#1', set(['cj', 'snd', 'prim', 'para', 'md', 'sys', 'prs', 'v', 'np', 'sg', 'op']))
('hari#1', set(['na', 'mas', 'sg', 'gen']))
('hari#1', set(['na', 'mas', 'abl', 'sg']))
('hari#1', set(['na', 'fem', 'sg', 'gen']))
('hari#1', set(['na', 'fem', 'abl', 'sg']))
('hari#2', set(['na', 'mas', 'sg', 'gen']))
('hari#2', set(['na', 'mas', 'abl', 'sg']))
('hari#2', set(['na', 'fem', 'sg', 'gen']))
('hari#2', set(['na', 'fem', 'abl', 'sg']))
```

#### Sandhi

```
$ python -m sanskrit_parser.lexical_analyzer.sandhi --join te eva
Joining te eva
set([u'teeva', u'taeva', u'ta eva', u'tayeva'])

$ python -m sanskrit_parser.lexical_analyzer.sandhi --split taeva 1
Splitting taeva at 1
set([(u'tar', u'eva'), (u'tas', u'eva'), (u'taH', u'eva'), (u'ta', u'eva')])

$ python -m sanskrit_parser.lexical_analyzer.sandhi --split taeva --all
All possible splits for taeva
set([(u't', u'aeva'), (u'tar', u'eva'), (u'taev', u'a'), (u'to', u'eva'), (u'ta', u'eva'), (u'te', u'eva'), (u'taH', u'eva'), (u'tae', u'va'), (u'taeva', u''), (u'tas', u'eva')])
```

#### MaheshvaraSutras

```
$ python -m sanskrit_parser.base.MaheshvaraSutras --encoding SLP1 --pratyahara jaS
aiuR fxk eoN EOc hayavaraw laR YamaNaRanam JaBaY GaQaDaz jabagaqadaS KaPaCaWaTacawatav kapay Sazasar hal
जश्
जबगडद

$ python -m sanskrit_parser.base.MaheshvaraSutras --encoding SLP1 --pratyahara jaS --varna k
aiuR fxk eoN EOc hayavaraw laR YamaNaRanam JaBaY GaQaDaz jabagaqadaS KaPaCaWaTacawatav kapay Sazasar hal
जश्
जबगडद
Is क् in जश्?
False

$ python -m sanskrit_parser.base.MaheshvaraSutras --encoding SLP1 --pratyahara jaS --varna g
aiuR fxk eoN EOc hayavaraw laR YamaNaRanam JaBaY GaQaDaz jabagaqadaS KaPaCaWaTacawatav kapay Sazasar hal
जश्
जबगडद
Is ग् in जश्?
True
```

## Sanskrit Parser Stack

Stack of parsing tools

### Level 0
Sandhi splitting subroutine 
       Input: Phoneme sequence and Phoneme number to split at 
       Action: Perform a sandhi split at given input phoneme number
       Ouptut:  left and right sequences (multiple options will be output). 
       No semantic validation will be performed (up to higher levels)
       
#### Current Status
Module that performs sandhi split/join and convenient rule definition is at `lexical_analyzer/sandhi.py`.

Rule definitions (human readable!) are at `lexical_analyzer/sandhi_rules/*.txt`

### Level 1
* From dhatu + lakAra + puruSha + vachana to pada and vice versa
* From prAtipadika + vibhakti + vachana to pada and vice versa
* Upasarga + dhAtu forms - forward and backwards
* nAmadhAtu forms
* Krt forms  - forwards and backwards
* Taddhita forms  - forwards and backwards

#### Current Status
To be done.

However, we have a usable solution with inriaxmlwrapper + Prof. Gerard Huet's forms database to act as queriable form database. That gives us the bare minimum we need from Level 1, so Level 2 can work.  

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
Module that performs sentence split is at `lexical_analyzer/SanksritLexicalAnalyzer.py`


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
Early experimental version (simple sentences only) is at `morphological_analyzer/SanskritMorphologicalAnalyzer.py`

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

