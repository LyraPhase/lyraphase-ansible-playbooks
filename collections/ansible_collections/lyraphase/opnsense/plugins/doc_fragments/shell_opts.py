# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

__metaclass__ = type

# Copyright 2025 LyraPhase LLC
# Copyright: (c) 2025, James Cuzella (@trinitronx)
# GNU Affero General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/agpl-3.0.txt)


class ModuleDocFragment(object):
    # Standard files documentation fragment
    DOCUMENTATION = r"""options:
  opnsense_shell_option:
    description: >
      Specifies the `opnsense-shell` choice to pass to the initial shell
      "`Enter an option: `" prompt.
    default: shell
    type: str
    choices:
      - shell
      - logout
      - assign_interfaces
      - set_interface_ip
      - reset_root_password
      - reset_to_factory_defaults
      - power_off
      - reboot
      - ping
      - pftop
      - firewall_log
      - reload_services
      - update
      - restore_backup
notes:
- For more information on using Ansible to manage network devices see the :ref:`Ansible
  Network Guide <network_guide>`
"""
