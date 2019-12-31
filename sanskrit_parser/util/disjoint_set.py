#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
""" Disjoint Set Data Structure

    Author: Karthik Madathil <kmadathil@gmail.com>
"""
from collections import defaultdict
from copy import copy

class DisjointSet(object):
    ''' Disjoint Set Class with Indexing'''
    def __init__(self, sets=None):
        self._data = defaultdict(lambda x: x)
        self._len  = 0
        self._sets = []
        if sets is not None:
            for st in sets:
                self.addset(st)

    def __len__(self):
        ''' Number of disjoint sets '''
        return len(self._sets)

    def __iter__(self):
        ''' Iterator '''
        return iter(self._sets)

    def __getitem__(self,ix):
        return self._sets[ix]
    
    def __repr__(self):
        return repr(self._sets)

    def addset(self,st):
        ''' Adds a set st to the DisjointSet. Representative element is whatever the set iterator returns first'''
        for (i,e) in enumerate(st):
            if i==0:
                parent = e
            self._data[e] = parent
        self._sets.append(st)

    def find(self, x):
        """
        Returns the representative member of the set of connected components to which x belongs, may be x itself.

        """
        if x != self._data[x]:
            self._data[x] = self.find(self._data[x])
        return self._data[x]

    def union(self, x, y):
        """
        Attaches the roots of x and y trees together if they are not the same already.
        :param x: first element
        :param y: second element
        :return: None
        """
        parent_x, parent_y = self.find(x), self.find(y)
        if parent_x != parent_y:
            self._data[parent_x] = parent_y
        for s in self._sets:
            if x in s:
                s_x = s
            if y in s:
                s_y = s
        s_x.update(s_y)
        self._sets.remove(s_y)

    def connected(self, x, y) -> bool:
        """
        :param x: first element
        :param y: second element
        :return: True if x and y belong to the same tree (i.e. they have the same root), False otherwise.
        """
        return self.find(x) == self.find(y)


    def remove(self, elems):
        ''' Removes elements from the Disjoint Set'''
        for e in elems:
            del self._data[e]
            newparent = None
            # Any elements with e as parent
            for k in self._data:
                if self._data[k] == e:
                    if newparent is None:
                        newparent = k
                self._data[k] = newparent
            for s in self._sets:
                if e in s:
                    s.remove(e)

    def copy(self):
        ''' Return a one-level deep copy '''
        t = DisjointSet()
        for s in self:
            t.addset(copy(s))
        return t
        
