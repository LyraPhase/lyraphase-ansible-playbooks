#!/usr/bin/env bash

# To be run inside an ansible execution environment container
# We must override any shell profile settings or paths here that might be
# imported from the user's home volume mount by ./bin/docker-run

# Use system python + ruby
command -v rbenv 1>/dev/null 2>&1 && export RBENV_VERSION='system'
command -v pyenv 1>/dev/null 2>&1 && export PYENV_VERSION='system'

# Just unload RVM b/c automatic loading of .ruby-version, .ruby-gemset,
# and .rvmrc is problematic when changing project directories
command -v rvm 1>/dev/null 2>&1 && typeset -f __rvm_unload 1>/dev/null 2>&1 && __rvm_unload && ruby_version_prompt() { :; }
if command -v rvm 1>/dev/null 2>&1 && ! typeset -f __rvm_unload 1>/dev/null 2>&1 || echo "$PATH" | grep -iq rvm; then
  # Remove RVM from path
  PATH="$(echo "$PATH" | tr ":" "\n" | grep -v rvm  | tr "\n" ":" | sed -e 's/:$//')"
  export PATH
  for var in $(env | grep -i rvm | sed -e 's/=.*$//g') ; do
    unset "$var"
  done
fi
