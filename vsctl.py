# coding=utf-8

# Copyright 2015 Brian J. Downs
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

OVS_CMD = 'ovs-vsctl'

"""
Library to configure ports and bridges as well as get information from the
system it's running against.

Some function descriptions taken from the ovs
man (8) pages or inspired by.
"""

#
# Bridge Functions
#


def list_bridges():
    """
    Gets all bridges currently configured in OVS.
    :return bridges: list
    """
    log.info("Getting all bridges")
    try:
        return filter(None, subprocess.Popen(
            [OVS_CMD, 'list-br'],
            stdout=subprocess.PIPE).communicate()[0].split('\n'))
    except subprocess.CalledProcessError, e:
        log.error(e.output)
        sys.exit(1)


def add_bridge(bridge):
    """
    Add provided bridge.
    :param bridge: str
    :return: bool
    """

    log.info("Adding bridge: {0}".format(bridge))
    try:
        subprocess.Popen(['{0} −−may−exist'.format(OVS_CMD), 'add-br', bridge],
                         stdout=subprocess.PIPE).communicate()
        log.info("Bridge: {0} added.".format(bridge))
        return True
    except subprocess.CalledProcessError, e:
        log.error(e.output)
        return False


def delete_bridge(bridge):
    """
    Delete provided bridge.
    :param bridge: str
    :return: bool
    """
    log.info("Deleting bridge: {0}".format(bridge))
    try:
        subprocess.Popen(['{0} −−if−exists'.format(OVS_CMD), 'del-br', bridge],
                         stdout=subprocess.PIPE).communicate()
        log.info("Bridge: {0} added.".format(bridge))
        return True
    except subprocess.CalledProcessError, e:
        log.error(e.output)
        return False


def bridge_to_vlan(bridge):
    pass

#
# Port Functions
#


def list_ports(bridge):
    """
    List ports on specified bridge.
    :param bridge: str
    :return: list
    """
    log.info("Listing ports on {0}".format(bridge))
    try:
        return filter(None, subprocess.Popen(
            [OVS_CMD, 'list-ports', bridge],
            stdout=subprocess.PIPE).communicate()[0].split('\n'))
    except subprocess.CalledProcessError, e:
        log.error(e.output)
        sys.exit(1)


def add_port(port, bridge, tag):
    """
    Add port to bridge as well as tag if provided.
    :param port: str
    :param bridge: str
    :param tag: int
    :return: bool
    """
    log.info("Adding port {0} on {1}".format(port, bridge))
    try:
        if tag:
            subprocess.Popen(
                ["{0} --may-exist".format(OVS_CMD),
                 bridge, port, "tag={0}".format(tag)]).communicate()
            return True
        subprocess.Popen(
            ["{0} --may-exist".format(OVS_CMD), bridge, port]
        ).communicate()
        return True
    except subprocess.CalledProcessError, e:
        log.error(e.output)
        return False


def delete_port(port, bridge=None):
    """
    Delete port from bridge if provided else delete any matching port.
    :param port: str
    :param bridge: str
    :return: bool
    """
    log.info("Deleting port: {0}".format(port))
    try:
        subprocess.Popen(["{0} --if-exists".format(OVS_CMD),
                         'del-port', bridge, port],
                         stdout=subprocess.PIPE).communicate()
    except subprocess.CalledProcessError, e:
        log.error(e)
        return False


def port_to_br(port):
    """
    Return bridge provided port resides on.
    :param port: str
    :return: str
    """
    try:
        return subprocess.Popen([OVS_CMD, 'port-to-br', port],
                                stdout=subprocess.PIPE).communicate()[0].strip('\n')
    except subprocess.CalledProcessError, e:
        log.error(e.output)
        sys.exit(1)
