# -*- coding: utf-8 -*-
# Copyright 2025 LyraPhase LLC
# Copyright 2025 James Cuzella (@trinitronx)
# GNU Affero General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/agpl-3.0.txt)

"""
The OPNsense legacy fact class
It is in this file the configuration is collected from the device
for a given resource, parsed, and the facts tree is populated
based on the configuration.
"""

from __future__ import absolute_import, division, print_function


__metaclass__ = type


import json
import platform
import re

from ansible.module_utils.common.text.converters import to_text
from ansible_collections.lyraphase.opnsense.plugins.module_utils.network.opnsense.shell import (
    get_capabilities,
    run_commands,
)


class FactsBase(object):
    COMMANDS = list()

    def __init__(self, module):
        self.module = module
        self.facts = dict()
        self.warnings = list()
        self.responses = None

    def populate(self):
        self.responses = run_commands(
            self.module,
            commands=self.COMMANDS,
            check_rc=False,
        )

    def run(self, cmd):
        return run_commands(self.module, commands=cmd, check_rc=False)


class Default(FactsBase):
    # COMMANDS = ["cat /usr/local/opnsense/version/core"] ## subset of firmware product metadata
    COMMANDS = ["configctl firmware product"]

    def populate(self):
        super(Default, self).populate()
        self.facts.update(self.platform_facts())
        data = self.responses[0]
        if data and (not isinstance(data, Exception)):
            product_data = json.loads(data)
            self.facts["opnsense_edition"] = (
                "opnsense-business" if "business" in product_data["product_id"] else "opnsense-community"
            )
            self.facts["product"] = product_data
            # self.facts["asatype"] = self.parse_asatype(data)
            # self.facts["serialnum"] = self.parse_serialnum(data)
            # self.parse_stacks(data)
        else:
            if isinstance(data, Exception):
                self.warnings.append("Unable to gather product information: %s" % to_text(data))

    def parse_asatype(self, data):
        match = re.search(r"Hardware:(\s+)ASA", data)
        if match:
            return "ASA"

    def parse_serialnum(self, data):
        match = re.search(r"Serial Number: (\S+)", data)
        if match:
            return match.group(1)

    # def parse_stacks(self, data):
    #   match = re.findall(r"^Model [Nn]umber\s+: (\S+)", data, re.M)
    #   if match:
    #       self.facts["stacked_models"] = match

    #   match = re.findall(
    #       r"^System [Ss]erial [Nn]umber\s+: (\S+)",
    #       data,
    #       re.M,
    #   )
    #   if match:
    #       self.facts["stacked_serialnums"] = match

    def platform_facts(self):
        platform_facts = {}

        resp = get_capabilities(self.module)
        device_info = resp["device_info"]
        platform_facts["system"] = device_info["network_os"]

        for item in (
            "model",
            "serialnum",
            "version",
            "freebsd_version",
            "unbound_version",
            "dhcpd_version",
            "kea_version",
            "openvpn_version",
            "sshd_version",
            "platform",
            "hostname",
        ):
            val = device_info.get("network_os_%s" % item)
            if val:
                platform_facts[item] = val

        platform_facts["api"] = resp["network_api"]
        platform_facts["python_version"] = platform.python_version()

        return platform_facts


class Hardware(FactsBase):
    COMMANDS = ["df -t nodevfs -T -k",
                "sysctl hw.realmem",
                "sysctl vm.stats",
                "vmstat -H"]

    def populate(self):
        warnings = list()
        super(Hardware, self).populate()
        data = self.responses[0]
        if data:
            self.facts["filesystems"] = self.parse_filesystems(data)
            self.facts["filesystems_info"] = self.parse_filesystems_info(data)

        data = self.responses[1]
        if data:
            if "sysctl: unknown oid" in data:
                warnings.append("Unable to gather amount of hardware total memory (hw.realmem)")
            else:
                if "hw.realmem:" in data:
                    (realmem_key, realmem_value) = data.split(":")
                    self.facts["hardware_realmem_mb"] = int(realmem_value.rstrip().lstrip()) // 1024 // 1024
                else:
                    warnings.append("Unable to gather amount of hardware total memory (hw.realmem)")

        data = self.responses[2]
        if data:
            for line in data.splitlines():
                (vm_stats_key, vm_stats_value) = line.split()
                if 'vm.stats.vm.v_page_size' in line:
                    pagesize = int(vm_stats_value)
                if 'vm.stats.vm.v_page_count' in line:
                    pagecount = int(vm_stats_value)
                if 'vm.stats.vm.v_free_count' in line:
                    freecount = int(vm_stats_value)
            self.facts['memtotal_mb'] = pagesize * pagecount // 1024 // 1024
            self.facts['memfree_mb'] = pagesize * freecount // 1024 // 1024
            self.facts["memused_mb"] = int(self.facts['memtotal_mb'] - self.facts['memfree_mb'])

        # Get free memory. vmstat output looks like:
        #  procs     memory       page                      disks faults       cpu
        #  r b w     avm     fre  flt  re  pi  po    fr   sr nv0   in   sy   cs us sy id
        #  0 0 0   47512   28160   51   0   0   1  1894   95   0  328   89   17  0  0 99
        data = self.responses[3]
        if data and not hasattr(self.facts, "memfree_mb"):
            if "vmstat: " in data:
                warnings.append("Unable to gather amount of used memory (vmstat 'fre')")
            else:
                if "fre" in data:
                    self.facts["memfree_mb"] = int(data.splitlines()[-1].split()[4]) // 1024
                else:
                    warnings.append("Unable to gather amount of physical memory (hw.physmem)")

    def parse_filesystems(self, data):
        return re.findall(r"^Directory of (\S+)/", data, re.M)

    def parse_filesystems_info(self, data):
        facts = dict()
        fs = ""
        for line in data.split("\n"):
            match = re.match(r"^Directory of (\S+)/", line)
            if match:
                fs = match.group(1)
                facts[fs] = dict()
                continue
            match = re.match(
                r"^(\d+) bytes total \((\d+) bytes free\/(\d+)% free\)",
                line,
            )
            if match:
                facts[fs]["spacetotal_kb"] = int(match.group(1)) / 1024
                facts[fs]["spacefree_kb"] = int(match.group(2)) / 1024

        return facts


class Packages(FactsBase):
    # COMMANDS = ["configctl firmware local"] ## Includes kernel & userland metadata also
    COMMANDS = ["pkg query '%n|||%v|||%c|||%sh|||%k|||%a|||%L|||%R|||%o'"]  # Just package metadata
    PKG_KEYS = [
        "name",
        "version",
        "comment",
        "size_human_readable",
        "locked",
        "automatically_installed",
        "licenses",
        "repository",
        "origin",
    ]

    def populate(self):
        warnings = list()
        data = self.responses[0]
        if data:
            self.facts["packages"] = self.parse_packages(data)

    def parse_packages(self, data):
        pkgs = []
        for line in data.rstrip().split("\n"):
            pkgs.append(dict(zip(self.PKG_KEYS, line.split("|||"))))
        return pkgs


class Config(FactsBase):
    COMMANDS = ["cat /usr/local/etc/config.xml"]

    def populate(self):
        super(Config, self).populate()
        data = self.responses[0]
        if data:
            self.facts["config"] = data
