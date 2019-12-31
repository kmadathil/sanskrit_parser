#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
""" Disjoint Set Data Structure

    Author: Karthik Madathil <kmadathil@gmail.com>
"""
from collections import defaultdict

class DisjointSet(object):
    ''' Disjoint Set Class '''
    def __init__(self, sets=None):
        self._data = defaultdict(lambda x: x)
        self._len  = 0
        if sets is not None:
            for st in sets:
                self.addset(st)

    def __iter__(self):
        for key in self._data:
            yield key, self.find(key)

    def __len__(self):
        ''' Number of disjoint sets '''
        return len(set(self._data.values()))

    def itersets(self):
        """
        Yields sets of connected components.
        """
        element_classes = defaultdict(lambda: set())
        for element in self._data:
            element_classes[self.find(element)].add(element)

        for element_class in element_classes.values():
            yield element_class

    def addset(self,st):
        ''' Adds a set st to the DisjointSet. Representative element is whatever the set iterator returns first'''
        for (i,e) in enumerate(st):
            if i==0:
                parent = e
            self._data[e] = parent

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
