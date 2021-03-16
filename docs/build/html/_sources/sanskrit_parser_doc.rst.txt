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

At this stage, have a valid split as per sandhi rules, but not
necessarily valid words in both halves. This is handled by the next stage.


Algorithm for Sandhi Split
..........................

We use a dynamic programming (memoized) algorithm to determine all possible
**valid** sandhi splits for a string.

#. Given a string, we scan it from left to right, and generate a list of all possible splits at each point (as defined in the previous section) as determined by our library of sandhi rules.
#. If the left hand split is a valid sanskrit word, we recursively split the right hand split using the same algorithm.
   
   #. This split is memoized as is expected in a dynamic programming algorithm
#. The result of this algorithm is a DAG (Directed Acyclic Graph) that represents all sandhi splits of the input string into valid words. *Each split does not need to correspond to a valid sentence (vAkya) at this stage. That constraint is handled by the next stage*.

For example, the string "अहङ्गच्छामि" results in the following DAG

.. image:: static/aham_gacCAmi.png

All graphs in this document have Sanskrit text encoded in SLP1_ format except if otherwise stated

.. _SLP1: https://en.wikipedia.org/wiki/SLP1

From this graph, each path between the beginning and the end nodes is a valid segmentation. When enumerating segmentations, we have two options

#. Prioritize paths with fewer number of words
#. Prioritize paths with a lower score (default). This uses a word2vec based scoring approach


Vakya Analysis / Dependency Parsing
-----------------------------------

The task of Vakya Analysis (Dependency Parsing) is to interpret a
sandhi split (segmentation) as a valid Sanskrit sentence if
possible. Each possible morpholgical interpretation of a word is
considered, and valid sentence interpretations are output. 

Algorithm for Vakya Analysis
.............................

Given a sandhi split of the input phrase into valid words, we

#. Determine all valid morphologies of each pada. For example, रामः could be the प्रथमा एकवचन form of राम, or the लट् उत्तमपुरुषबहुवचनम् form of the verb रा. Only dependency parsing will tell us which form is relevant to the current sentence.
#. The Sandhi Graph from the previous stage is transformed into a Vakya Graph, which is a k-partite graph with each partition containing the possible morphologies of each word. For example, the input रामो ग्रामं याति, which is split as रामः ग्रामम् याति results in this: :ref:`kpgraph`
#. Edges are added between nodes in different partitions, so that each edge describes a possible grammatical relationship.
#. A modified version of Kruskal's algorithm is used to extract all Generalized Spanning Trees (GST) of the k-partite Vakya Graph. A GST is defined as a tree that contains exactly one node of each partition in the k-partite Vakya Graph.
#. A global constraint checker checks consistency of each GST against a set of rules.
#. Each such GST will be a valid parse of the sentence. For example: :ref:`parsegraph`

Graphs
+++++++

.. _kpgraph:

.. figure:: static/rama_split0.dot.png
   :width: 800
	      
   k-partite graph for रामः ग्रामम् याति 

.. _parsegraph:

.. figure:: static/rama_split0_parse0.dot.png
   :width: 800

   A minimum Cost Parse Graph for रामः ग्रामम् याति

.. _parsegraph2:

.. figure:: static/pustakam_split0_parse20.dot.png
   :width: 800

   A minimum Cost Parse Graph for "अहम् तस्मै पुस्तकम् अददम्"

Edges
......

We add the following set of edges



Modified Kruskal Algorithm
--------------------------


GST Constraint Checks
----------------------
