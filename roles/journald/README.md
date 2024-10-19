Role: journald
==============

**Description:**

This role will:

- Configure & restart JournalD

Requirements
------------

**Supports:**

- YoctoLinux - Intel Edison 3.0

**Assumptions:**

This role makes the assumption that the `systemd-journald` service exists on the
system. This should be already installed on Intel Edison's Yocto Linux image.

**Required Variables:**

- `journald_conf_settings` - (dict) Required by `journald.conf.j2` Jinja2
  template for `/etc/systemd/journald.conf` settings.  Define these as
  `key: value` pairs.

Role Variables
--------------

The default role variables in `defaults/main.yml` are:

```YAML
---
# journald: entry point for defaults
journald_conf_settings:
  storage: persistent
```

Dependencies
------------

None.

Example Playbook
----------------

```YAML
---
# This playbook deploys the journald role

- hosts: foo

  roles:
    - journald
```

License
-------

[AGPLv3][1]

Author Information
------------------

Copyright (C) © 🄯  2014-2024 LyraPhase.com / 37Om.com / 37Ohm.com
Copyright (C) © 🄯  2014-2024 James Cuzella <@trinitronx>

[1]: http://choosealicense.com/licenses/agpl-3.0/
