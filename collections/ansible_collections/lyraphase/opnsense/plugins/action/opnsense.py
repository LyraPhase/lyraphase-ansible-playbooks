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

from ansible_collections.ansible.netcommon.plugins.action.network import ActionModule as ActionNetworkModule


class ActionModule(ActionNetworkModule):
    def run(self, tmp=None, task_vars=None):
        # BEGIN DEBUG INSTRUMENTATION
        # import debugpy

        # debugpy.listen(5678)
        # debugpy.wait_for_client()
        # debugpy.breakpoint()
        # END DEBUG INSTRUMENTATION
        del tmp  # tmp no longer has any effect

        module_name = self._task.action.split(".")[-1]
        # TODO: remove config modules
        self._config_module = True if module_name in ["opnsense_config", "config"] else False
        persistent_connection = self._play_context.connection.split(".")[-1]
        warnings = []

        if persistent_connection not in ("network_cli", "libssh"):
            return {
                "failed": True,
                "msg": "Connection type %s is not valid for this module" % self._play_context.connection,
            }

        result = super(ActionModule, self).run(task_vars=task_vars)
        if warnings:
            if "warnings" in result:
                result["warnings"].extend(warnings)
            else:
                result["warnings"] = warnings
        return result
