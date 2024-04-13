Role: openwrt-dumbap-base
==================

**Description:**

A base role to setup OpenWRT as a dumb Wifi Access Point

This role will:

- Install `arp-scan` package dependency on OpenWRT via `opkg`
- Install a `crontabs/root` file to run `arp-scan` periodically to resolve hostnames for
  Associated Stations (WiFi clients)
- Disable DHCP on `br-lan`
- Set static IP and network settings according to variables `openwrt_dumbap_static_lan`

Requirements
------------

**Supports:**

- OpenWRT / LEDE

**Assumptions:**

This role makes the assumption that the `opkg` command exists on the system.
For `--check` mode to work properly, you must have already run the tasks in
`openwrt-python.yml` of `openwrt-base` role once.

**Required Variables:**

- `openwrt_dumbap_opkg_packages` - Required by `openwrt-dumbap-base` role.
- `openwrt_dumbap_static_lan` - Required to setup static IP + network settings.

Role Variables
--------------

The default role variables in `vars/default.yml` are:

```YAML
# openwrt-dumbap-base: entry point for defaults
# default.yml - default vars for unsupported / unknown OS
# (Assumes this is OpenWRT LEDE Image)
---
openwrt_dumbap_opkg_packages:
  - arp-scan

```

- `openwrt_dumbap_opkg_packages` - List of `opkg` packages to install.
- `openwrt_dumbap_static_lan` - Required to setup static IP + network settings.

- `openwrt_opkg_packages` - List of `opkg` repository feed definition files to install.
  - Default Packages:
    - `arp-scan`: ARP scan utility used by the crontab to resolve hostnames.

Dependencies
------------

This role depends on the following OpenWRT base packages:

- `opkg`
- `libc`
- `libpthread`
- `libubox`
- `uclient-fetch`

Example Playbook
----------------

```YAML
---
# This playbook deploys the openwrt-dumbap-base role

- hosts: openwrt
  user: root
  gather_facts: no

  roles:
    - openwrt-dumbap-base
```

License
-------

[GPLv3][1]

Author Information
------------------

Copyright (C) © 🄯  2014-2024 LyraPhase.com / 37Om.com
Copyright (C) © 🄯  2014-2024 James Cuzella <@trinitronx>

[1]: http://choosealicense.com/licenses/gpl-3.0/
