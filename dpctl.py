# coding=utf-8

# Copyright 2014 Brian J. Downs <brian.downs@gmail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sys
import logging
import subprocess

log = logging.getLogger(__name__)

OVS_CMD = 'ovs-dpctl'

"""
This library provides basic access to create, modify and delete Open vSwitch
datapaths.

Some function descriptions taken from the ovs
man (8) pages or inspired by.
"""


def add_dp(dp, netdev=None):
    """
    Create dp on netdev if provided.
    :param dp: str
    :param netdev: str
    :return: bool
    """
    netdev = netdev if netdev else None
    log.info("Creating dp: {0}".format(dp))
    try:
        if netdev:
            subprocess.Popen([OVS_CMD, 'add-dp', dp, netdev], stdout=subprocess.PIPE).communicate()
            log.info("{0} created.".format(dp))
            return True
        subprocess.Popen([OVS_CMD, 'add-dp', dp], stdout=subprocess.PIPE).communicate()
        log.info("{0} created.".format(dp))
        return True
    except subprocess.CalledProcessError, e:
        log.error(e.output)
        return False


def del_dp(dp):
    """
    Delete provided datapath.
    :param dp: str
    :return: bool
    """
    log.info("Deleting {0}".format(dp))
    try:
        subprocess.Popen([OVS_CMD, 'del-dp', dp], stdout=subprocess.PIPE).communicate()
        return True
    except subprocess.CalledProcessError, e:
        log.error(e.output)
        return False


def add_if(dp, netdev, if_type, key):
    """
    Adds provided interface along with interface details if provided.
    :param dp: str
    :param netdev: str
    :param if_type: str
    :param key: str
    :return:
    """
    if_type = if_type if if_type else None
    key = key if key else None
    log.info("Adding interface: {0}".format(0))
    try:
        if if_type and key:
            subprocess.Popen([OVS_CMD, 'add-if', netdev, dp, if_type, key], stdout=subprocess.PIPE).communicate()
            return True
        if if_type:
            subprocess.Popen([OVS_CMD, 'add-if', netdev, dp, if_type], stdout=subprocess.PIPE).communicate()
            return True
        if key:
            subprocess.Popen([OVS_CMD, 'add-if', netdev, dp, key], stdout=subprocess.PIPE).communicate()
            return True
        subprocess.Popen([OVS_CMD, 'add-if', netdev, dp], stdout=subprocess.PIPE).communicate()
        return True
    except subprocess.CalledProcessError, e:
        log.error(e.output)
        sys.exit(1)


def del_if(dp, netdev):
    """
    Removes each netdev from the list of network devices datapath dp
    monitors.
    :param dp: str
    :param netdev: list
    :return: bool
    """
    log.info("Deleting interface(s) from {0}".format(dp))
    try:
        map(lambda nd: subprocess.Popen(
            [OVS_CMD, 'del-if', dp, nd],
            stdout=subprocess.PIPE).communicate(), netdev)
        return True
    except subprocess.CalledProcessError, e:
        log.error(e.output)
        return False


def dump_dps():
    """
    Print all datapaths
    :return: str
    """
    log.info("Dumping datapaths")
    try:
        return subprocess.Popen([OVS_CMD, 'dump-dps'], stdout=subprocess.PIPE).communicate()
    except subprocess.CalledProcessError, e:
        log.error(e.output)
        sys.exit(1)


def show(dp=None):
    """
    Prints  a  summary  of  configured  datapaths with details.
    :param dp: str
    :return: str
    """
    dp = dp if dp else None
    log.info("Dumping flows for: {0}".format(0))
    try:
        if dp:
            return subprocess.Popen([OVS_CMD, 'show'], stdout=subprocess.PIPE).communicate()
        return subprocess.Popen([OVS_CMD, 'show', dp], stdout=subprocess.PIPE).communicate()
    except subprocess.CalledProcessError, e:
        log.error(e.output)
        sys.exit(1)


def dump_flows(dp):
    """
    Print flows for provided dataflow.
    :param dp: str
    :return: str
    """
    log.info("Dumping flows for: {0}".format(0))
    try:
        return subprocess.Popen([OVS_CMD, 'dump-flows', dp], stdout=subprocess.PIPE).communicate()
    except subprocess.CalledProcessError, e:
        log.error(e.output)
        sys.exit(1)


def del_flows(dp):
    """
    Delete all flows from provided datapath.
    :param dp: str
    :return: bool
    """
    log.info("Deleting flow from: {0}".format(0))
    try:
        subprocess.Popen([OVS_CMD, 'del-flows', dp], stdout=subprocess.PIPE).communicate()
        return True
    except subprocess.CalledProcessError, e:
        log.error(e.output)
        return False