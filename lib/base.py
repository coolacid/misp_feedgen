#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import itertools

class baseclass:
    def __init__(self, config, output_config):
        pass

    @staticmethod
    def compare(list1, list2):
        list1 = set(map(tuple,list1))
        list2 = set(map(tuple,list2))
        return list1 == list2

    @staticmethod
    def diff(list1, list2):
        list1 = set(map(tuple,list1))
        list2 = set(map(tuple,list2))
        return list1 ^ list2

    @staticmethod
    def unroll(r):
        options = []
        for x in r:
            if not isinstance(x, list) and not isinstance(x, tuple):
                options.append([x])
            else:
                options.append(x)
        options = list(map(list,itertools.product(*options)))
        return options
