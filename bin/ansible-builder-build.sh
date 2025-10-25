#!/bin/sh

TAG="${TAG:-lyraphase/ansible-playbooks-ee}"

ansible-builder build -v3 -t "$TAG" "$@"
