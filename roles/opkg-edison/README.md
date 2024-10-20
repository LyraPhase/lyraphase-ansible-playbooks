Role: opkg-edison
=================

**Description:**

This role will:

- Make your favorite breakfast sandwich

Requirements
------------

**Supports:**

- YoctoLinux - Intel Edison 3.0

**Assumptions:**

This role makes the assumption that the `foo` command exists on the system.
Install this with the `foo` role.

**Required Variables:**

- `opkg-edison_foo` - Required by `opkg-edison` role.
- `opkg-edison_dependency_bar_baz` - Required by dependency
  `opkg-edison-dependency-bar` role.

Role Variables
--------------

The default role variables in `defaults/main.yml` are:

```YAML
---
# opkg-edison: entry point for defaults
opkg-edison_foo: true
```

- `opkg-edison_foo` - Allows foo-barring for opkg-edison.

Dependencies
------------

This role depends on the following roles:

- `opkg-edison-dependency-bar`

Example Playbook
----------------

```YAML
---
# This playbook deploys the opkg-edison role

- hosts: foo

  roles:
    - opkg-edison
```

License
-------

[AGPLv3][1]

Author Information
------------------

Copyright (C) © 🄯  2014-2024 LyraPhase.com / 37Om.com
Copyright (C) © 🄯  2014-2024 James Cuzella <@trinitronx>

[1]: http://choosealicense.com/licenses/agpl-3.0/
