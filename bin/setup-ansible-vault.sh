#!/bin/bash

[[ "${ANSIBLE_EE}" == 1 ]] && source /etc/profile.d/setup-ansible-ee-docker-env.sh

ANSIBLE_VAULT_PASSWORD_FILE=$(which lastpass-ansible)
export ANSIBLE_VAULT_PASSWORD_FILE

if ! lpass status 1>/dev/null 2>&1 ; then
  _this_shell=$(ps -p $$ | awk '$1 != "PID" {print $4}')
  if [[ "$_this_shell" == 'zsh' ]]; then
    _read_cmd="LPASS_USERNAME=\$(zsh -c 'vared -c -p '\''Enter LastPass login email: '\'' LPASS_USERNAME ; printf %s \"\$LPASS_USERNAME\"')"
    echo "$_read_cmd"
  else
    _read_cmd="read -r -p 'Enter LastPass login email: ' LPASS_USERNAME"
  fi
  [ -n "$LPASS_USERNAME" ] || eval "$_read_cmd"
  lpass login "$LPASS_USERNAME"
fi
