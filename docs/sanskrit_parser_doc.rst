Documentation
=========================================

Introduction
------------

The goal of the sanskrit_parser project is to create a freely reusable open
source sanskrit parser and generator. This is intended to be usable as a
python library for other tools that need sanskrit parsing and generation, as
well as providing basic command line and web user interfaces for basic tasks.

We aim to be

* Freely reusable (the more the merrier)
* Open Source
* Classical - We favour traditional grammar over statistical methods,
   but use statistical methods where necessary and helpful.


Sandhi Split / Segmentation
---------------------------

Given a phrase, the goal is to be able to generate all valid
segmentations (sandhi splits) such that each segment is a valid
Sanskrit word (pada).

For this, we first need a pada dictionary. We currently use a
combination of open source data from the sanskrit_data_ project and
the `Sanskrit Heritage project of INRIA`_. 

.. _sanskrit_data: https://github.com/avinashvarna/sanskrit_forms
.. _`Sanskrit Heritage project of INRIA`:  https://gitlab.inria.fr/huet/Heritage_Resources

This will be eventually replaced by our own Paninian Pada generator when that
is complete.


Sandhi Rules
............

Paninian Sandhi rules have been implemented as a set of matching rules
which define how sandhi transformations work.

For example the famous इको यणचि (६.१.७७) rule is implemented thus ::
  
 # यण्-सन्धिः
 # इको यणचि (६.१.७७)
 [*हल्][इ, ई] + [*अच् - इई][*हल्+ं] = {0}य्{2}{3}
 [*हल्][उ, ऊ] + [*अच् - उऊ][*हल्+ं] = {0}व्{2}{3}
 [*हल्][ऋ, ॠ] + [*अच् -ऋॠऌ][*हल्+ं] = {0}र्{2}{3}
 [*हल्][ऌ]+ [*अच् -ऋॠऌ][*हल्+ं] = {0}ल्{2}{3}

Since these rules are defined in terms of Paninian pratyaharas such as
``[*हल्]``, these are internally expanded into multiple sub-rules. Each
subrule will end up with a defined sequence of characters on its right
hand side.

If a substring match with exactly that sequence is found,
then the left hand side of the same subrule, suitably extended by the
substring prefix and suffix is output as a possible split.

At this stage, we do not worry about whether the strings output are valid.


Algorithm for Sandhi Split
..........................

We use a dynamic programming (memoized) algorithm to determine all possible
**valid** sandhi splits for a string.

#. Given a string, we scan it from left to right, and generate a list of all possible splits at each point (as defined in the previous section) as determined by our library of sandhi rules.
#. If the left hand split is a valid sanskrit word, we recursively split the right hand split using the same algorithm.
   
   #. This split is memoized as is expected in a dynamic programming algorithm
#. The result of this algorithm is a DAG (Directed Acyclic Graph) that represents all sandhi splits of the input string into valid words. *Note that each split does not need to correspond to a valid sentence (vAkya) at this stage*.

For example, the string "अहङ्गच्छामि" results in the following DAG

.. image:: static/aham_gacCAmi.png

All graphs in this document have Sanskrit text encoded in SLP1_ format except if otherwise stated

.. _SLP1: https://en.wikipedia.org/wiki/SLP1

From this graph, each path between the beginning and the end nodes is a valid segmentation. When enumerating segmentations, we have two options

#. Prioritize paths with fewer number of words
#. Prioritize paths with a lower score (default). This uses a word2vec based scoring approach
