#!/usr/bin/python
# -*- coding: utf-8 -*-

import pathlib
import os
import yaml
import bunch

RAW_CONFIG = yaml.full_load(open(os.path.join(pathlib.Path(__file__).parent.resolve(), "config.yaml")).read())
CONFIG = bunch.bunchify(RAW_CONFIG)


def main():
    pass
