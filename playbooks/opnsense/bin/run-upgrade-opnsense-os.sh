#!/bin/bash

SCRIPT=$(basename "$0")
REPO_BASE=$( cd "$( dirname "${BASH_SOURCE[0]}" )/.." && pwd )

# If using docker-machine + VirtualBox...
# Hack for forcing mdns / Bonjour / Zeroconf DNS resolution to be done on the Host machine running the VM
# Resolve from docker-machine VM -> OSX Host -> mDNS (local LAN segment which edisons are attached to)
DOCKER_MACHINE_NAME=$(docker-machine active 2>/dev/null)

if [ -n "${DOCKER_MACHINE_NAME}" ]; then
  VBoxManage modifyvm "$DOCKER_MACHINE_NAME" --natdnshostresolver1 on
fi

# Assuming you set up SSH keys, SSH in as root via key auth
ANSIBLE_STDOUT_CALLBACK=debug ansible-playbook -i "${REPO_BASE}"/inventory/hosts "${REPO_BASE}"/upgrade-opnsense-os.yml -vv --diff --ask-become-pass
