#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
""" Disjoint Set Data Structure for Kruskals Algorithm

    Author: Karthik Madathil <kmadathil@gmail.com>
"""
from copy import copy


class DisjointSet(object):
    ''' Disjoint Set Class with Indexing'''
    def __init__(self):
        self._data = {}

    def find(self, x):
        """
        Returns the representative member of the set of connected components to which x belongs, may be x itself.

        """
        if x not in self._data:
            self._data[x] = x
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
        if x == y:
            return
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

    def copy(self):
        ''' Return a one-level deep copy '''
        t = DisjointSet()
        # for s in self:
        #     t.addset(copy(s))
        t._data = copy(self._data)
        return t
