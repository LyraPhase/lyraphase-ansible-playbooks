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
  become:
    description:
    - The become option will instruct the CLI session to attempt privilege
      escalation on platforms that support it. Normally this means transitioning
      from user mode to `enable` mode in the CLI session for a network device.
      For OPNsense firewall devices with CLI over SSH, the FreeBSD-based OS
      supports `sudo` like a typical Unix host.
      If become is set to `True` and the remote device does not support
      privilege escalation or the privilege has already been elevated, then this
      option is silently ignored.
    type: bool
  become_method:
    description:
    - This option allows the `become` method to be specified in for handling
      privilege escalation. Typically the `become_method` value is set to
      `enable` for network devices. For OPNsense firewall devices, it should be
      defined as `sudo`.
      Defaults to `sudo`
    type: str
notes:
- For more information on using Ansible to manage network devices see the :ref:`Ansible
  Network Guide <network_guide>`
"""
