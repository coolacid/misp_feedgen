#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import subprocess
from lib.base import baseclass

class postrun_shell(baseclass):
    def __init__(self, config, hook_config, feedname):
        self.config = config
        self.hook_config = hook_config
        self.feedname = feedname

    def hook(self):
        shell = False
        if isinstance(self.hook_config['command'], str):
            shell = True
        elif isinstance(self.hook_config['command'], list):
            shell = False
        else:
            logging.error("Command must be a string, or list, see subprocess.run")
            return
        output = subprocess.run(self.hook_config['command'], stdout = subprocess.PIPE, text = True, shell=shell)
        for line in output.stdout.split("\n"):
            logging.debug(line)
