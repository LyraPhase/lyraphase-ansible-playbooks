#!/bin/bash

SCRIPT=$(basename "$0")
PLAYBOOK_BASE=$( cd "$( dirname "${BASH_SOURCE[0]}" )/.." && pwd )
REPO_BASE=$( cd "${PLAYBOOK_BASE}/../../" && pwd )

ansible-galaxy collection install -r "${REPO_BASE}/requirements.yml"
ansible-galaxy role install -r "${REPO_BASE}/requirements.yml"
