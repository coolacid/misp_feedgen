#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import itertools

class baseclass:
    def __init__(self, config, output_config):
        pass

    def unroll(self,r):
        options = []
        for x in r:
            if not isinstance(x, list) and not isinstance(x, tuple):
                options.append([x])
            else:
                options.append(x)
        options = list(map(list,itertools.product(*options)))
        return options
