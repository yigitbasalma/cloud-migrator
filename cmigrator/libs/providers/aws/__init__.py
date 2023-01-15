#!/usr/bin/python
# -*- coding: utf-8 -*-

from importlib import import_module

import boto3

from cmigrator import CONFIG

PROVIDER_CONFIG = CONFIG.source if CONFIG.source.provider == "aws" else CONFIG.destination


boto3.setup_default_session(
    profile_name=PROVIDER_CONFIG.profile
)

_ = boto3.client("ec2", region_name=PROVIDER_CONFIG.region)
__ = _.describe_regions()

# Defaults
REGIONS = {
    i["RegionName"]: i["Endpoint"]
    for i in __["Regions"]
}

# Account resources
_ = boto3.client("iam", region_name=PROVIDER_CONFIG.region)
ACCOUNT_ID = _.list_users()["Users"][0]["Arn"].split(":")[4]


def controller():
    for target in CONFIG.targets:
        _module = import_module(f"cmigrator.libs.providers.{PROVIDER_CONFIG.provider}.{target}")
        _module.start()
