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
        self.mock_shell_get_capabilities = patch(
            "ansible_collections.lyraphase.opnsense.plugins.module_utils.network.opnsense.shell.get_capabilities",
        )
        self.shell_get_capabilities = self.mock_shell_get_capabilities.start()
        self.shell_get_capabilities.return_value = {
            "device_info": OPNsenseDeviceInfo.MOCK_DEVICE_INFO.copy(),
        }

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
        capabilities_return_value = OPNsenseDeviceInfo.MOCK_DEVICE_INFO.copy()
        capabilities_return_value.update(
            {
                "network_api": "ansible.netcommon.libssh",
                "device_info": OPNsenseDeviceInfo.MOCK_DEVICE_INFO.copy(),
            },
        )
        self.get_capabilities.return_value = capabilities_return_value

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

    def test_opnsense_facts_platform_facts(self):
        set_module_args({"gather_subset": "default"})
        result = self.execute_module()
        # self.log("Result: %s" % result, 4)
        expected = {
            "ansible_net_system": "opnsense",
            "ansible_net_version": "24.4.3",
            "ansible_net_freebsd_version": "13.2-RELEASE-p12",
            "ansible_net_unbound_version": "1.20.0",
            "ansible_net_hostname": "OPNsense.internal",
            "ansible_net_api": "ansible.netcommon.libssh",
            "ansible_net_python_version": "3.12.11",
            "ansible_net_opnsense_edition": "opnsense-business",
        }
        for key, value in expected.items():
            self.assertEqual(result["ansible_facts"][key], value)

    def test_opnsense_facts_product(self):
        set_module_args({"gather_subset": "default"})
        self.maxDiff = None
        expected = {
            "ansible_net_product": {
                "product_abi": "24.4",
                "product_arch": "amd64",
                "product_check": None,
                "product_copyright_owner": "Deciso B.V.",
                "product_copyright_url": "https://www.deciso.com/",
                "product_copyright_years": "2014-2024",
                "product_email": "project@opnsense.org",
                "product_hash": "deefa5e05",
                "product_id": "opnsense-business",
                "product_latest": "24.4.3",
                "product_license": {"valid_to": "2026-05-06"},
                "product_log": 1,
                "product_mirror": "https://opnsense-update.deciso.com/${SUBSCRIPTION}/FreeBSD:13:amd64/24.4",
                "product_name": "OPNsense",
                "product_nickname": "Savvy Shark",
                "product_repos": "OPNsense",
                "product_series": "24.4",
                "product_tier": "1",
                "product_time": "Thu Sep 19 20:13:17 MDT 2024",
                "product_version": "24.4.3",
                "product_website": "https://opnsense.org/",
            },
        }
        result = self.execute_module()
        # self.log("Result: %s" % result, 4)
        self.assertEqual(result["ansible_facts"]["ansible_net_product"], expected["ansible_net_product"])

    @unittest.skip("TODO: implement filesystems info facts + tests")
    def test_opnsense_facts_filesystems_info(self):
        # TODO: Gather FS facts
        pass
        # "ansible_net_filesystems": ["/", "/var", "/tmp", "/usr", "/usr/local", "/home", "/boot/efi"],
        # Current:
        #   'ansible_net_filesystems': [], 'ansible_net_filesystems_info': {},
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

    def test_opnsense_facts_hardware(self):
        set_module_args({"gather_subset": "hardware"})
        result = self.execute_module()
        expected = {
            "ansible_net_memtotal_mb": 15740,
            "ansible_net_memfree_mb": 9920,
            "ansible_net_memused_mb": 5817,
        }
        for key, value in expected.items():
            self.assertEqual(result["ansible_facts"][key], value)
