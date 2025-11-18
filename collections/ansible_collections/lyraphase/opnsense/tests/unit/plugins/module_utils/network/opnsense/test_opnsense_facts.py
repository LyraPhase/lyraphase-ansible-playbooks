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
import unittest

from unittest.mock import patch

from ansible_collections.lyraphase.opnsense.plugins.modules import opnsense_facts
from ansible_collections.lyraphase.opnsense.tests.unit.mock.device_info import OPNsenseDeviceInfo
from ansible_collections.lyraphase.opnsense.tests.unit.plugins.modules.opnsense_module import (
    TestOPNsenseModule,
    load_fixture,
)
from ansible_collections.lyraphase.opnsense.tests.unit.plugins.modules.utils import (
    set_module_args,
)


class TestOPNsenseFactsModule(TestOPNsenseModule):
    module = opnsense_facts

    def setUp(self):
        super(TestOPNsenseFactsModule, self).setUp()
        self.mock_run_commands = patch(
            "ansible_collections.lyraphase.opnsense.plugins.module_utils.network.opnsense.facts.legacy.base.run_commands",
        )
        self.run_commands = self.mock_run_commands.start()

        self.mock_get_resource_connection = patch(
            "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.facts.facts.get_resource_connection",
        )
        self.get_resource_connection = self.mock_get_resource_connection.start()

        self.mock_get_capabilities = patch(
            "ansible_collections.lyraphase.opnsense.plugins.module_utils.network.opnsense.facts.legacy.base.get_capabilities",
        )
        self.get_capabilities = self.mock_get_capabilities.start()
        self.get_capabilities.return_value = OPNsenseDeviceInfo.MOCK_DEVICE_INFO.copy().update(
            {
                "network_api": "cliconf",
            }
        )

    def tearDown(self):
        super(TestOPNsenseFactsModule, self).tearDown()
        self.mock_run_commands.stop()
        self.mock_get_capabilities.stop()

    def load_fixtures(self, commands=None):
        def load_from_file(*args, **kwargs):
            commands = kwargs["commands"]
            output = []

            for command in commands:
                filename = str(command).split(" | ", 1)[0].replace(" ", "_")
                output.append(load_fixture("opnsense_facts_%s" % filename))
            return output

        self.run_commands.side_effect = load_from_file

    @unittest.skip("TODO: implement base facts + tests")
    def test_opnsense_facts_base(self):
        set_module_args({"gather_subset": "default"})
        result = self.execute_module()
        self.assertEqual(
            result["ansible_facts"]["ansible_net_opnsense_edition"],
            "opnsense-business",
        )
        self.assertEqual(result["ansible_facts"]["ansible_net_system"], "opnsense")

    @unittest.skip("TODO: implement filesystems info facts + tests")
    def test_opnsense_facts_filesystems_info(self):
        # TODO
        pass
        set_module_args({"gather_subset": "hardware"})
        result = self.execute_module()
        self.assertEqual(
            result["ansible_facts"]["ansible_net_filesystems_info"]["zroot"]["spacetotal_kb"],
            204075048.0,
        )
        self.assertEqual(
            result["ansible_facts"]["ansible_net_filesystems_info"]["zroot"]["spacefree_kb"],
            201488732.0,
        )
