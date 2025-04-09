#!/bin/bash

ANSIBLE_VAULT_PASSWORD_FILE=$(which lastpass-ansible)
export ANSIBLE_VAULT_PASSWORD_FILE

if ! lpass status 1>/dev/null 2>&1 ; then
  [ -n "$LPASS_USERNAME" ] || read -r -p 'Enter LastPass login email: ' LPASS_USERNAME
  lpass login "$LPASS_USERNAME"
fi

