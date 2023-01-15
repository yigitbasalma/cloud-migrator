#!/usr/bin/python
# -*- coding: utf-8 -*-

from importlib import import_module

import pathlib
import logging
import coloredlogs
import os
import yaml
import bunch

# Define constraints
RAW_CONFIG = yaml.full_load(open(os.path.join(pathlib.Path(__file__).parent.resolve(), "config.yaml")).read())
CONFIG = bunch.bunchify(RAW_CONFIG)

# Init logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                    level=logging.getLevelName(CONFIG.logging.level))
coloredlogs.install()
LOGGER = logging.getLogger("cmigrator.main")


def main():
    LOGGER.info(f"Initializing source providers. Source Provider: {CONFIG.source.provider}, "
                f"Destination Provider: {CONFIG.destination.provider}")

    # Define provider modules
    _source = import_module(f"cmigrator.libs.providers.{CONFIG.source.provider}")
    LOGGER.info("Source provider is initialized.")
    _destination = import_module(f"cmigrator.libs.providers.{CONFIG.destination.provider}")
    LOGGER.info("Destination provider is initialized.")

    LOGGER.info("Starting to the source controller.")
    _source.controller()
