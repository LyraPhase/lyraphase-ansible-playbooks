# -*- coding: utf-8 -*-
# Copyright 2025 LyraPhase LLC
# Copyright 2025 James Cuzella (@trinitronx)
# GNU Affero General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/agpl-3.0.txt)
from __future__ import absolute_import, division, print_function

from ansible.module_utils._text import to_text
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.connection import Connection
from ansible_collections.lyraphase.opnsense.plugins.module_utils.network.opnsense.providers import providers


__metaclass__ = type


class NetworkModule(AnsibleModule):
    fail_on_missing_provider = True

    def __init__(self, connection=None, *args, **kwargs):
        super(NetworkModule, self).__init__(*args, **kwargs)

        if connection is None:
            connection = Connection(self._socket_path)

        self.connection = connection
        if self.connection._network_os is None:
            self.connection._network_os = "lyraphase.opnsense.shell"

    @property
    def provider(self):
        if not hasattr(self, "_provider"):
            capabilities = self.from_json(self.connection.get_capabilities())
            self.debug("Capabilities: %s" % to_text(capabilities, errors="surrogate_then_replace"))

            network_os = capabilities["device_info"]["network_os"]
            network_api = capabilities["network_api"]

            if network_api == "cliconf":
                connection_type = "network_cli"
            else:
                connection_type = "ansible.netcommon.libssh"

            cls = providers.get(
                network_os,
                self._name.split(".")[-1],
                connection_type,
            )
