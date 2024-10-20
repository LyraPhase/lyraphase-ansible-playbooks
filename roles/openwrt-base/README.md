Role: openwrt-base
==================

**Description:**

This role will:

- Install minimal Ansible dependencies on OpenWRT via `python-lite`
- Install any `opkg` repository feeds listed in `openwrt_opkg_repo_files`
- Install any `opkg` packages listed in `openwrt_opkg_packages`

Requirements
------------

**Supports:**

- OpenWRT / LEDE

**Assumptions:**

This role makes the assumption that the `opkg` command exists on the system.
For `--check` mode to work properly, you must have already run the tasks in
`openwrt-python.yml` once.

**Required Variables:**

- `openwrt_opkg_packages` - Required by `openwrt-base` role.
- `opkg-edison_dependency_bar_baz` - Required by dependency
  `opkg-edison-dependency-bar` role.

Role Variables
--------------

The default role variables in `defaults/main.yml` are:

```YAML
# opkg-edison: entry point for defaults
# default.yml - default vars for unsupported / unknown OS
# (Assumes this is OpenWRT LEDE Image)
---
openwrt_opkg_repo_files:
  - distfeeds.conf
  - customfeeds.conf

openwrt_opkg_packages:
  - ca-certificates
  - ca-bundle
  - zlib
  - libopenssl
  - curl
  - uclient-fetch
```

- `opkg_repo_files` - List of `opkg` repository feed definition files to install.
- `openwrt_opkg_packages` - List of `opkg` repository feed definition files to install.
  - Default Packages:
    - `ca-certificates`: System CA certificates
    - `ca-bundle`: System CA certificates as a bundle
    - `zlib`: zlib is a lossless data-compression library
    - `libopenssl`: This package contains the OpenSSL shared libraries, needed
      by other programs
    - `curl`: A client-side URL transfer utility
    - `uclient-fetch`: Tiny `wget` replacement using `libuclient`

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
# This playbook deploys the openwrt-base role

- hosts: openwrt
  user: root
  gather_facts: no

  roles:
    - openwrt-base
```

License
-------

[AGPLv3][1]

Author Information
------------------

Copyright (C) © 🄯  2014-2024 LyraPhase.com / 37Om.com
Copyright (C) © 🄯  2014-2024 James Cuzella <@trinitronx>

[1]: http://choosealicense.com/licenses/agpl-3.0/
