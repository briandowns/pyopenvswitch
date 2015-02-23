# Copyright 2014 Brian J. Downs
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

"""
Overview

pyopenvswitch is a library to control and interact with
[Open vSwitch](openvswitch.org) installations.

This library implements the following components of the Open vSwitch software
package:

- vsctl
- ofctl
- dpctl

Requirements

- Open vSwitch 1.10 or higher

Installation

pip install pyopenvswitch

Examples

>>> from pyopenvswitch import vsctl
>>> vsctl.list_bridges()
>>> from pyopenvswitch import ofctl
>>> ofctl.ping()
>>> from pyopenvswitch import dpctl
>>> dpctl.dump_flows()
"""
