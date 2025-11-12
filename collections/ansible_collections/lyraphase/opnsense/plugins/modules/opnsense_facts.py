#!/usr/bin/python
#
# -*- coding: utf-8 -*-
# Copyright 2025 LyraPhase LLC
# Copyright 2025 James Cuzella (@trinitronx)
#
# This file is part of LyraPhase OPNsense Collection
#
# LyraPhase OPNsense Collection is free software: you can redistribute it and/or
# modify it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# LyraPhase OPNsense Collection is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with LyraPhase OPNsense Collection.
# If not, see <http://www.gnu.org/licenses/>.
#
from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = """
module: facts
author:
- James Cuzella (@trinitronx)
short_description: Collect facts from remote devices running OPNsense
description:
- Collects a base set of device facts from a remote device that is running OPNsense.
  This module prepends all of the base network fact keys with C(ansible_net_<fact>).
  The facts module will always collect a base set of facts from the device and can
  enable or disable collection of additional facts.
- Note, to collect facts from OPNsense device properly, the user should elevate the
  privilege to become root or admin group.
version_added: 1.0.0
extends_documentation_fragment:
- lyraphase.opnsense.become
notes:
- Tested against OPNsense 24.4.3
options:
  gather_subset:
    description:
    - When supplied, this argument restricts the facts collected to a given subset.
    - Possible values for this argument include C(all), C(min), C(hardware), C(config).
    - Specify a list of values to include a larger subset.
    - Use a value with an initial C(!) to collect all facts except that subset.
    required: false
    type: list
    elements: str
    default: '!config'
  gather_network_resources:
    description:
    - When supplied, this argument will restrict the facts collected to a given subset.
      Possible values for this argument include all and the resources like interfaces,
      vlans etc. Can specify a list of values to include a larger subset. Values can
      also be used with an initial C(!) to specify that a specific subset should
      not be collected. Values can also be used with an initial C(!) to specify
      that a specific subset should not be collected. Valid subsets are 'all', **TODO** '??', '??'.
    required: false
    type: list
    elements: str
"""

EXAMPLES = """
- name: Gather all legacy facts
  lyraphase.opnsense.facts:
    gather_subset: all

- name: Gather only the config and default facts
  lyraphase.opnsense.facts:
    gather_subset:
      - config

- name: Do not gather hardware facts
  lyraphase.opnsense.facts:
    gather_subset:
      - '!hardware'

- name: Gather legacy and resource facts
  lyraphase.opnsense.facts:
    gather_subset: all
"""

RETURN = """
ansible_net_gather_subset:
  description: The list of fact subsets collected from the device
  returned: always
  type: list

# default
ansible_net_model:
  description: The model name returned from the device
  returned: always
  type: str
ansible_net_serialnum:
  description: The serial number of the remote device
  returned: always
  type: str
ansible_net_version:
  description: The OPNsense operating system version running on the remote device
  returned: always
  type: str
ansible_net_freebsd_version:
  description: The base FreeBSD operating system version running on the remote device.
  returned: always
  type: str
ansible_net_opnsense_edition:
  description: The OPNsense operating system edition running on the remote device
               also called "package name" (e.g. opnsense-business, opnsense-community)
  returned: always
  type: str
ansible_net_unbound_version:
  description: The Unbound DNS daemonversion running on the remote device.
  returned: always
  type: str
ansible_net_dhcpd_version:
  description: The ISC DHCP daemon version running on the remote device.
  returned: always
  type: str
ansible_net_kea_version:
  description: The KEA daemon version running on the remote device.
  returned: always
  type: str
ansible_net_openvpn_version:
  description: The OpenVPN daemon version running on the remote device.
  returned: always
  type: str
ansible_net_sshd_version:
  description: The SSH daemon version running on the remote device.
  returned: always
  type: str
ansible_net_hostname:
  description: The configured hostname of the device
  returned: always
  type: str
ansible_net_api:
  description: The name of the transport
  returned: always
  type: str
ansible_net_python_version:
  description: The Python version Ansible controller is using
  returned: always
  type: str

# packages
ansible_net_packages:
  description: The list of packages installed on the device.
  returned: when packages is configured for facts module
  type: list

# network
## TODO: check - rely on main setup module (works on FreeBSD?)

# hardware
ansible_net_filesystems:
  description: All file system names available on the device
  returned: when hardware is configured
  type: list
ansible_net_filesystems_info:
  description: A hash of all file systems containing info about each file system (e.g. free and total space)
  returned: when hardware is configured
  type: dict
ansible_net_memfree_mb:
  description: The available free memory on the remote device in Mb
  returned: when hardware is configured
  type: int
ansible_net_memused_mb:
  description: The used memory on the remote device in Mb
  returned: when hardware is configured
  type: int
ansible_net_memtotal_mb:
  description: The total memory on the remote device in Mb
  returned: when hardware is configured
  type: int

# config
ansible_net_config:
  description: The current active config from the device
  returned: when config is configured
  type: str
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.lyraphase.opnsense.plugins.module_utils.network.opnsense.argspec.facts.facts import (
    FactsArgs,
)
from ansible_collections.lyraphase.opnsense.plugins.module_utils.network.opnsense.facts.facts import (
    Facts,
)
from ansible_collections.lyraphase.opnsense.plugins.module_utils.network.opnsense.shell import (
    shell_argument_spec,
)


def main():
    """
    Main entry point for module execution

    :returns: ansible_facts
    """
    argument_spec = FactsArgs.argument_spec
    argument_spec.update(shell_argument_spec)

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
    )

    warnings = []
    if module.params["gather_subset"] == "!config":
        warnings.append(
            "default value for `gather_subset` will be changed to `min` from `!config` v2.11 onwards",
        )

    result = Facts(module).get_facts()

    ansible_facts, additional_warnings = result
    warnings.extend(additional_warnings)

    module.exit_json(ansible_facts=ansible_facts, warnings=warnings)


if __name__ == "__main__":
    main()
