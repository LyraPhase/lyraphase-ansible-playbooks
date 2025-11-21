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
---
author: James Cuzella (@trinitronx)
name: shell
short_description: Use opnsense shell to run command on the OPNsense platform
description:
- This opnsense plugin provides low level abstraction apis for sending and receiving CLI
  commands from OPNsense network devices using opnsense-shell.
version_added: 1.0.0
extends_documentation_fragment:
- lyraphase.opnsense.become
"""

import json
import re

from ansible.errors import AnsibleConnectionFailure


try:
    from ansible.module_utils.common.text.converters import to_bytes, to_text
except ImportError:
    from ansible.module_utils._text import to_bytes, to_text

from ansible_collections.ansible.netcommon.plugins.plugin_utils.terminal_base import TerminalBase


class TerminalModule(TerminalBase):
    terminal_stdout_re = [
        re.compile(rb"\w+\@[\w\-\.]+:[^\]] ?[>#\$%] ?$"),
        re.compile(rb"^[\r\n]?[\w+\-\.:\/\[\]@~ ]+[#%\$] ?(?:.*?[\r\n](?:[^>\)\?]*?)?[>#\?] ?)*", re.MULTILINE),
    ]

    terminal_stderr_re = [
        re.compile(rb"error:", re.I),
        re.compile(rb"Permission denied, please try again\."),
        re.compile(
            rb"Received disconnect from .*? port (?:\d+:?\d+)?: Too many authentication failures$",
        ),
        re.compile(rb"\w+: Command not found\.$"),
        re.compile(rb"\w+: : Permission denied$"),
        re.compile(rb"^Command authorization failed\r?$", re.MULTILINE),
    ]

    # N/A for OPNsense
    # terminal_config_prompt = re.compile(r"^.+\(config(-.*)?\)#$")

    def on_open_shell(self):
        if self._get_prompt().strip().endswith(b"#"):
            self.disable_pager()

    def disable_pager(self):
        try:
            self._exec_cli_command("no terminal pager")
        except AnsibleConnectionFailure:
            raise AnsibleConnectionFailure("unable to disable terminal pager")

    def on_become(self, passwd=None):
        if self._get_prompt().strip().endswith(b"#"):
            return

        cmd = {"command": "enable"}
        if passwd:
            # Note: python-3.5 cannot combine u"" and r"" together.  Thus make
            # an r string and use to_text to ensure it's text on both py2 and py3.
            cmd["prompt"] = to_text(
                r"[\r\n]?[Pp]assword: $",
                errors="surrogate_or_strict",
            )
            cmd["answer"] = passwd

        try:
            self._exec_cli_command(
                to_bytes(json.dumps(cmd), errors="surrogate_or_strict"),
            )
        except AnsibleConnectionFailure:
            raise AnsibleConnectionFailure(
                "unable to elevate privilege to enable mode",
            )

        self.disable_pager()
