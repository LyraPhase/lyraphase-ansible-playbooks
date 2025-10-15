# shellcheck shell=sh
[ -d "${XDG_CONFIG_HOME:-$HOME/.config}"/bat/themes ] && command -v bat 1>/dev/null 2>&1 && bat cache --build
