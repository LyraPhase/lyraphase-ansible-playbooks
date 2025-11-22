# -*- coding: utf-8 -*-
# Copyright 2025 LyraPhase LLC
# Copyright 2025 James Cuzella (@trinitronx)
# GNU Affero General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/agpl-3.0.txt)
"""
The arg spec for the opnsense facts module.
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type


class FactsArgs(object):
    """The arg spec for the opnsense facts module"""

    def __init__(self, **kwargs):
        pass

    argument_spec = {
        "gather_subset": dict(
            default=["!config"],
            type="list",
            elements="str",
        ),
        "gather_network_resources": dict(type="list", elements="str"),
        "passwords": {"type": "bool", "default": False},
        "opnsense_shell_option": {
            "type": "str",
            "default": "shell",
            "choices": [
                "shell",
                "logout",
                "assign_interfaces",
                "set_interface_ip",
                "reset_root_password",
                "reset_to_factory_defaults",
                "power_off",
                "reboot",
                "ping",
                "pftop",
                "firewall_log",
                "reload_services",
                "update",
                "restore_backup",
            ],
        },
    }
