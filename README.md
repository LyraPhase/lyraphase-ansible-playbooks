<!-- markdownlint-configure-file
{
  "required-headings": {
    "headings": [
      "# lyraphase-ansible-playbooks",
      "*"
    ]
  }
}
-->

lyraphase-ansible-playbooks
===========================

[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![pre-commit](https://github.com/LyraPhase/sprout-wrap/actions/workflows/pre-commit.yml/badge.svg)](https://github.com/trinitronx/lyraphase-ansible-playbooks/actions/workflows/pre-commit.yml)

This repository contains all of the Ansible-based
playbooks used for LyraPhase network devices, and
IoT (Raspberry Pi, PiKVM, Intel Edison) staging activities.

The basic directory layout mostly follows [Ansible's Best
Practices](http://www.ansibleworks.com/docs/playbooks_best_practices.html).

    ops-ansible-playbooks/
    |-- ansible.cfg         # The main ansible configuration file.
    |-- bin/                # Generic utility scripts used by Ansible
    |-- inventory/          # All inventory file and scripts must be here.
    |   `-- group_vars/    # Variables to apply to 'groups' go here.
    |   `-- host_vars/     # Variables to apply to individual hosts go here.
    |-- library/            # Custom or non-core modules go here.
    |-- playbooks/          # All of our playbooks go in sub-directories here.
    `-- roles/             # All actual role code goes here.

A LyraPhase / 37Om specific style guide is located in the [docs](/docs/STYLE_GUIDE.md/)
