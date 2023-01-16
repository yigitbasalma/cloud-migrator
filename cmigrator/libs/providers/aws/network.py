#!/usr/bin/python
# -*- coding: utf-8 -*-

import boto3
import logging

from . import PROVIDER_CONFIG


class Provider:
    LOGGER = logging.getLogger("provider.aws.network")
    CLIENT = boto3.client("ec2", region_name=PROVIDER_CONFIG.region)
    RESOURCE = boto3.resource("ec2", region_name=PROVIDER_CONFIG.region)
    RESULT = []

    def get_resources(self):
        for vpc in self.CLIENT.describe_vpcs()["Vpcs"]:
            _vpc_object = self.RESOURCE.Vpc(vpc["VpcId"])
            _vpc = dict(cidr=_vpc_object.cidr_block, id=_vpc_object.vpc_id, original_tags=_vpc_object.tags,
                        is_default=_vpc_object.is_default, subnets=[], route_tables=[], internet_gatways=[],
                        nat_gateways=[])
            for subnet in _vpc_object.subnets.all():
                _subnet_object = self.RESOURCE.Subnet(subnet.id)
                _vpc["subnets"].append(dict(cidr_block=_subnet_object.cidr_block,
                                            map_public_ip_on_launch=_subnet_object.map_public_ip_on_launch,
                                            id=_subnet_object.subnet_id, tags=_subnet_object.tags))
            for route_table in _vpc_object.route_tables.all():
                _route_table_object = self.RESOURCE.RouteTable(route_table.id)
                _vpc["route_tables"].append(dict(id=_route_table_object.route_table_id,
                                                 subnets=[
                                                     i.get("SubnetId") for i in
                                                     _route_table_object.associations_attribute
                                                 ],
                                                 tags=_route_table_object.tags,
                                                 routes=_route_table_object.routes_attribute))
            for internet_gateway in _vpc_object.internet_gateways.all():
                _internet_gateway_object = self.RESOURCE.InternetGateway(internet_gateway.id)
                _vpc["internet_gatways"].append(dict(id=internet_gateway.id, tags=internet_gateway.tags))
            self.RESULT.append(_vpc)

        return self.RESULT
