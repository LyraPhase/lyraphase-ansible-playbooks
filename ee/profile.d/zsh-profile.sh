# shellcheck shell=sh
# Source all *.zsh files & zsh.local
for i in /etc/profile.d/*.zsh /etc/profile.d/zsh.local ; do
    if [ -r "$i" ]; then
        if [ "${-#*i}" != "$-" ]; then
            # shellcheck source=/dev/null
            . "$i"
        else
            # shellcheck source=/dev/null
            . "$i" >/dev/null
        fi
    fi
done
