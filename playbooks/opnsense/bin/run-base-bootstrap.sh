#!/bin/bash

SCRIPT=$(basename "$0")
PLAYBOOK_BASE=$( cd "$( dirname "${BASH_SOURCE[0]}" )/../" && pwd )
REPO_BASE=$( cd "$( dirname "${BASH_SOURCE[0]}" )/../../../" && pwd )
ROLE_NAME=$(basename "$(cd "$( dirname "${BASH_SOURCE[0]}" )/.." && pwd)" )
source "${REPO_BASE}/bin/setup-ansible-vault.sh"

echo "${ROLE_NAME}: ${SCRIPT}"

# If using docker-machine + VirtualBox...
# Hack for forcing mdns / Bonjour / Zeroconf DNS resolution to be done on the Host machine running the VM
# Resolve from docker-machine VM -> OSX Host -> mDNS (local LAN segment which edisons are attached to)
DOCKER_MACHINE_NAME=$(docker-machine active 2>/dev/null)

if [ -n "${DOCKER_MACHINE_NAME}" ]; then
  VBoxManage modifyvm "$DOCKER_MACHINE_NAME" --natdnshostresolver1 on
fi

# First run must SSH in as root with asked password (we assume you have set a password first)
ansible-playbook -i "${PLAYBOOK_BASE}"/inventory/hosts "${PLAYBOOK_BASE}"/base.yml -vv --tags=bootstrap --diff --user=root --ask-pass "$@"
