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

OVS_CMD = 'ovs-ofctl'

"""
Monitoring and administering OpenFlow switches.

Some function descriptions taken from the ovs
man (8) pages or inspired by.
"""

#
# OpenFlow Switch Management Commands
#


def show(switch):
    """
    Print out information for provided switch.
    :param switch: str
    :return: str
    """
    log.info("Showing details for {0}".format(switch))
    try:
        return subprocess.Popen([OVS_CMD, 'show', switch], stdout=subprocess.PIPE).communicate()
    except subprocess.CalledProcessError, e:
        log.error(e.output)
        sys.exit(1)


def status(switch, key=None):
    """
    Print out key/value pairs for the provided swtich status. If key is provided, only
    that data will be shown.
    :param switch: str
    :param key: str
    :return: str
    """
    log.info("Printing status for switch {0}".format(switch))
    try:
        if key:
            return subprocess.Popen([OVS_CMD, 'status', switch, key], stdout=subprocess.PIPE).communicate()
        return subprocess.Popen([OVS_CMD, 'status', switch], stdout=subprocess.PIPE).communicate()
    except subprocess.CalledProcessError, e:
        log.error(e.output)
        sys.exit(1)


def dump_tables(switch):
    """
    Print table statistics for the flow tables for the given switch.
    :param switch: str
    :return: str
    """
    log.info("Showing table statistics for switch {0}".format(switch))
    try:
        return subprocess.Popen([OVS_CMD, 'dump-tables', switch], stdout=subprocess.PIPE).communicate()
    except subprocess.CalledProcessError, e:
        log.error(e.output)
        sys.exit(1)


def dump_ports(switch, netdev=None):
    """
    Show statistics for the provided switch.
    :param switch: str
    :param netdev: str
    :return: str
    """
    log.info("Showing port statistics for switch {0}".format(switch))
    try:
        if switch:
            return subprocess.Popen([OVS_CMD, 'dump-ports', switch], stdout=subprocess.PIPE).communicate()
        return subprocess.Popen([OVS_CMD, 'dump-ports', switch, netdev], stdout=subprocess.PIPE).communicate()
    except subprocess.CalledProcessError, e:
        log.error(e.output)
        sys.exit(1)


def mod_port(switch, netdev, action):
    """
    Modify interface on switch.
    :param switch: str
    :param netdev: str
    :param action:str
    :return: bool
    """
    log.info("Modifying device: {0}".format(netdev))
    try:
        subprocess.Popen([OVS_CMD, 'mod-port', switch, netdev, action], stdout=subprocess.PIPE).communicate()
        return True
    except subprocess.CalledProcessError, e:
        log.error(e.output)
        return False


def dump_flows(switch, flows=None):
    """
    Show all flows on switch.  If flows is provided, will show flows associated.
    :param switch: str
    :param flows: str
    :return: str
    """
    flows = flows if flows else None
    log.info("Dumping flows for: {0}".format(switch))
    try:
        if flows:
            return subprocess.Popen([OVS_CMD, 'dump-flows', switch, flows],
                                    stdout=subprocess.PIPE).communicate()
        return subprocess.Popen([OVS_CMD, 'dump-flows', switch], stdout=subprocess.PIPE).communicate()
    except subprocess.CalledProcessError, e:
        log.error(e.output)
        sys.exit(1)


def dump_aggregate(switch, flows=None):
    """
    Print aggregate statistics for flows in switch.  Only print flows that
    match flows if provided.
    :param switch: str
    :param flows: str
    :return: str
    """
    flows = flows if flows else None
    try:
        if flows:
            return subprocess.Popen([OVS_CMD, 'dump-aggregate', switch, flows],
                                    stdout=subprocess.PIPE).communicate()
        return subprocess.Popen([OVS_CMD, 'dump-aggregate', switch], stdout=subprocess.PIPE).communicate()
    except subprocess.CalledProcessError, e:
        log.error(e.output)
        sys.exit(1)


def queue_stats(switch, port=None, queue=None):
    """
    Print stats for all ports and queues.  If port and queue are provided,
    results are modified to only the relevant stats.
    :param switch: str
    :param port: str
    :param queue: str
    :return: str
    """
    port = port if port else None
    queue = queue if queue else None
    try:
        if port:
            if queue:
                return subprocess.Popen([OVS_CMD, 'queue-stats', switch, port, queue],
                                        stdout=subprocess.PIPE).communicate()
            return subprocess.Popen([OVS_CMD, 'queue-stats', switch, port],
                                    stdout=subprocess.PIPE).communicate()
        return subprocess.Popen([OVS_CMD, 'queue-stats', switch],
                                stdout=subprocess.PIPE).communicate()
    except subprocess.CalledProcessError, e:
        log.error(e.output)
        sys.exit(1)


def add_flow(switch, flow):
    """
    Add flow to given switch.
    :param switch: str
    :param flow: str
    :return: bool
    """
    try:
        subprocess.Popen([OVS_CMD, 'add-flow', switch, flow], stdout=subprocess.PIPE).communicate()
        return True
    except subprocess.CalledProcessError, e:
        log.error(e.output)
        return False


def add_flows(switch, flow_file):
    """
    Add flows to given switch.
    :param switch: str
    :param flow_file: str
    :return: bool
    """
    try:
        subprocess.Popen([OVS_CMD, 'add-flows', switch, flow_file], stdout=subprocess.PIPE).communicate()
        return True
    except subprocess.CalledProcessError, e:
        log.error(e.output)
        return False


def mod_flows(switch, flow):
    """
    Modify the actions in entries  from  the  switch's  tables  that match  flow.
    :param switch: str
    :param flow: str
    :return: bool
    """
    try:
        subprocess.Popen([OVS_CMD, 'mod-flows', switch, flow], stdout=subprocess.PIPE).communicate()
        return True
    except subprocess.CalledProcessError, e:
        log.error(e.output)
        return False


def del_flows(switch, flow=None):
    """
    Deletes  entries from the switch's tables that match flow.
    :param switch: str
    :param flow: str
    :return: bool
    """
    try:
        if flow:
            subprocess.Popen([OVS_CMD, 'del-flows', switch, flow], stdout=subprocess.PIPE).communicate()
            return True
        subprocess.Popen([OVS_CMD, 'del-flows', switch], stdout=subprocess.PIPE).communicate()
        return True
    except subprocess.CalledProcessError, e:
        log.error(e.output)
        return False


def snoop(switch):
    switch = switch if switch else None
    raise NotImplementedError


def monitor(switch, miss_len=None):
    switch = switch if switch else None
    raise NotImplementedError

#
# OpenFlow Switch and Controller Commands
#


def probe(target):
    """
    Sends a single OpenFlow echo-request message to target
    and waits for the response.
    :param target: str
    :return: str
    """
    log.info("Probing {0}".format(target))
    try:
        return subprocess.Popen(["{0} -t".format(OVS_CMD), 'probe', target],
                                stdout=subprocess.PIPE).communicate()
    except subprocess.CalledProcessError, e:
        log.error(e.output)
        sys.exit(1)


def ping(target, packet_size=None):
    """
    Sends  a  series  of 10 echo request packets to target
    and times each reply
    :param target: str
    :param packet_size: int
    :return: str
    """
    log.info("Pinging {0}".format(target))
    try:
        if packet_size:
            return subprocess.Popen([OVS_CMD, 'ping', target, packet_size],
                                    stdout=subprocess.PIPE).communicate()
        return subprocess.Popen([OVS_CMD, 'ping', target], stdout=subprocess.PIPE).communicate()
    except subprocess.CalledProcessError, e:
        log.error(e.output)
        sys.exit(1)


def benchmark(target, packet_size, count):
    """
    Sends count  echo  request  packets  that  each  consist  of  an
    OpenFlow  header  plus  n  bytes  of  payload and waits for each
    response.
    :return: str
    """
    log.info("Printing benchmark information.")
    try:
        return subprocess.Popen([OVS_CMD, 'benchmark', packet_size, count],
                                stdout=subprocess.PIPE).communicate()
    except subprocess.CalledProcessError, e:
        log.error(e.output)
        sys.exit(1)