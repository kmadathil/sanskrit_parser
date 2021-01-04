#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Intro
======
Get varnas in a pratyahara:

.. code:: python

    >>> from sanskrit_parser.base.maheshvara_sutra import MaheshvaraSutras
    >>> MS = MaheshvaraSutras()
    >>> jaS = SanskritImmutableString('jaS', encoding=SLP1)
    >>> print(MS.getPratyahara(jaS))
    jabagaqada

Check if a varna is in a pratyahara:

.. code:: python

    >>> g = SanskritImmutableString('g')
    >>> print(MS.isInPratyahara(jaS, g))
    True
    >>> k = SanskritImmutableString('k')
    >>> print(MS.isInPratyahara(jaS, k))
    False



Command line usage
==================

::

    $ python -m sanskrit_parser.base.maheshvara_sutra --encoding SLP1 --pratyahara jaS
    aiuR fxk eoN EOc hayavaraw laR YamaNaRanam JaBaY GaQaDaz jabagaqadaS KaPaCaWaTacawatav kapay Sazasar hal
    जश्
    जबगडद

"""

from __future__ import print_function
from . import sanskrit_base
import re
import six


class MaheshvaraSutras(object):
    """
    Singleton MaheshvaraSutras class
    Attributes:
    MS(SanskritImmutableString) : Internal representation of mAheshvara sutras
    MSS(str)           : Canonical (SLP1) representation
    """

    def __init__(self):
        """
        Initialize Maheshvara Sutras object
        """
        # Note that a space is deliberately left after each it to help in
        # demarcating them.
        self.MS = sanskrit_base.SanskritImmutableString(
            u'अइउण् ऋऌक् एओङ् ऐऔच् हयवरट् लण् ञमङणनम् झभञ् घढधष् जबगडदश् खफछठथचटतव् कपय् शषसर् हल् ',
            sanskrit_base.DEVANAGARI)
        # SLP1 version for internal operations
        self.MSS = self.MS.canonical()

    def __str__(self):
        # Use SLP1 for default string output
        return self.MSS

    def getPratyahara(self, p, longp=True, remove_a=False, dirghas=False):
        """
        Return list of varnas covered by a pratyahara

        Args:
              p(:class:SanskritImmutableString): Pratyahara
              longp(boolean :optional:): When True (default), uses long pratyaharas
              remove_a(boolean :optional:): When True, removes intermediate 'a'.This is better for computational use
              dirghas(boolean :optional:) When True (default=False) adds dirgha vowels to the returned varnas
        Returns:
              (SanskritImmutableString): List of varnas to the same encoding as p
        """

        # SLP1 encoded pratyahara string
        ps = p.canonical()
        # it - halantyam
        pit = ps[-1]
        # Non it - all except it
        pnit = ps[:-1]
        # Non it position
        pnpos = self.MSS.find(pnit)
        # It position - space added to match it marker in internal
        # representation
        if longp:  # Find last occurence of it
            pitpos = self.MSS.rfind(pit + ' ', pnpos)
        else:  # Find first occurence of it
            pitpos = self.MSS.find(pit + ' ', pnpos)
        # Substring. This includes intermediate its and spaces
        ts = self.MSS[pnpos:pitpos]
        # Replace its and spaces
        ts = re.sub('. ', '', ts)
        # Remove अकारः मुखसुखार्थः
        if remove_a:
            ts = ts[0] + ts[1:].replace('a', '')
        # Add dIrgha vowels if requested
        if dirghas:
            ts = ts.replace('a', 'aA').replace('i', 'iI').replace('u', 'uU').replace('f', 'fF').replace('x', 'xX')
        return sanskrit_base.SanskritImmutableString(ts, sanskrit_base.SLP1)

    def isInPratyahara(self, p, v, longp=True):
        """
        Checks whether a given varna is in a pratyahara

        Args:
            p(SanskritImmutableString): Pratyahara
            v(SanskritImmutableString): Varna
            longp(boolean :optional:): When True (default), uses long pratyaharas
        Returns
             boolean: Is v in p?
        """

        vs = v.canonical()
        # १ . १ . ६९ अणुदित् सवर्णस्य चाप्रत्ययः
        # So, we change long and pluta vowels to short ones in the input string
        # Replace long vowels with short ones (note SLP1 encoding)
        vs = re.sub('[AIUFX]+', lambda m: m.group(0).lower(), vs)
        # Remove pluta
        vs = vs.replace('3', '')

        # Convert Pratyahara into String
        # the 'a' varna needs special treatment - we remove the
        # अकारः मुखसुखार्थः before searching!
        pos = self.getPratyahara(p, longp, remove_a=vs[0] == 'a').canonical()

        # Check if varna String is in Pratyahara String
        return (pos.find(vs) != -1)

    def isSavarna(self, v, a):
        """
        Checks whether a given varna "a" is savarna to another "v"

        Args:
            v(SanskritImmutableString): Varna Indicator
            a(SanskritImmutableString): Varna

        v can be a svara (in which case we return True irrespective of length
        of a)
        v can be an udit, in which we return True for anything in the group
        v can be tapara in which we return true only for the right length

        Returns
             boolean: Is v savarna to p?
        """
        ac = a.canonical()
        vc = v.canonical()

        # Single
        if len(vc) == 1:
            # १ . १ . ६९ अणुदित् सवर्णस्य चाप्रत्ययः
            # So, we change long and pluta vowels to short ones in the input string
            # Replace long vowels with short ones (note SLP1 encoding)
            ac = re.sub('[AIUFX]+', lambda m: m.group(0).lower(), ac)
            # Remove pluta
            ac = ac.replace('3', '')
            vc = re.sub('[AIUFX]+', lambda m: m.group(0).lower(), vc)
            # Remove pluta
            vc = vc.replace('3', '')
            return ac == vc
        elif vc[-1] == "t":
            # taparastatkAlasya
            return ac == vc[:-1]
            # FIXME implment tkArsya para interpretation
        elif vc[-1] == "u":
            # १ . १ . ६९ अणुदित् सवर्णस्य चाप्रत्ययः
            if vc[0] == "k":
                vc = "kKgGN"
            elif vc[0] == "c":
                vc = "cCjJY"
            elif vc[0] == "w":
                vc = "wWqQR"
            elif vc[0] == "t":
                vc = "tTdDn"
            elif vc[0] == "p":
                vc = "pPbBm"
            return ac in vc
        else:
            return ac in vc


if __name__ == "__main__":
    import argparse

    def getArgs():
        """
          Argparse routine.
          Returns args variable
        """
        # Parser Setup
        parser = argparse.ArgumentParser(description='SanskritImmutableString')
        # Pratyahara - print out the list of varnas in this
        parser.add_argument('--pratyahara', type=str, default="ik")
        # Varna. Optional. Check if this varna is in pratyahara above
        parser.add_argument('--varna', type=str, default=None)
        # Encoding Optional
        parser.add_argument('--encoding', type=str, default=None)
        # Short pratyaharas
        parser.add_argument('--short', action='store_true')
        # Remove intermediate as
        parser.add_argument('--remove-a', action='store_true')
        # Include dIrghas when returning the pratyAhAra
        parser.add_argument('--dirghas', action='store_true', default=False)
        parser.add_argument('--output-slp1', action='store_true')

        return parser.parse_args()

    def main():
        args = getArgs()
        m = MaheshvaraSutras()
        print(m)
        if args.encoding is not None:
            e = sanskrit_base.SCHEMES[args.encoding]
        else:
            e = None
        p = sanskrit_base.SanskritImmutableString(args.pratyahara, e)
        longp = not args.short
        if args.output_slp1 is False:
            print(six.text_type(p.devanagari()))
            print(six.text_type(m.getPratyahara(p, longp, args.remove_a, args.dirghas).devanagari()))
        else:
            print(six.text_type(p.canonical()))
            print(six.text_type(m.getPratyahara(p, longp, args.remove_a, args.dirghas).canonical()))
        if args.varna is not None:
            v = sanskrit_base.SanskritImmutableString(args.varna, e)
            print(u"Is {} in {}?".format(v.devanagari(),
                                         p.devanagari()))
            print(m.isInPratyahara(p, v, longp))

    main()
