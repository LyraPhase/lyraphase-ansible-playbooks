# shellcheck shell=sh
export XDG_CACHE_HOME="${XDG_CACHE_HOME:-/var/run/user/$(id -u)/cache}"
if [ -n "$ZSH_NAME" ]; then
  export ZSH_CACHE_DIR="${XDG_CACHE_HOME}/zsh"
  export ZSH_COMPDUMP="${ZSH_CACHE_DIR}/zcompcache/.zcompdump-${ZSH_VERSION}"
fi
