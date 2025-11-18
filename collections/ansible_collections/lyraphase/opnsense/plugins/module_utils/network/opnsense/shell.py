# This code is part of LyraPhase OPNsense Collection, but is an independent
# component.
# This particular file snippet, and this file snippet only, is BSD licensed.
# Modules you write using this snippet, which is embedded dynamically by Ansible
# still belong to the author of the module, and may assign their own license
# to the complete work.
#
# (c) 2025 LyraPhase LLC
# (c) 2025 James Cuzella (@trinitronx)
#
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#
#    * Redistributions of source code must retain the above copyright
#      notice, this list of conditions and the following disclaimer.
#    * Redistributions in binary form must reproduce the above copyright notice,
#      this list of conditions and the following disclaimer in the documentation
#      and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
# IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE
# USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
from __future__ import absolute_import, division, print_function


__metaclass__ = type
import json

from ansible.module_utils._text import to_text
from ansible.module_utils.connection import Connection, ConnectionError, exec_command
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.utils import (
    EntityCollection,
)


_DEVICE_CONFIGS = {}
_CONNECTION = None

command_spec = {"command": {"key": True}, "prompt": {}, "answer": {}}

shell_argument_spec = {
    "opnsense_shell_option": {"type": "str"},
    "passwords": {"type": "bool"},
}


def check_args(module):
    """Ensure specific args are set

    :return: None: In case all arguments passed are valid
    """
    # no args to check
    pass


def get_connection(module):
    if hasattr(module, "_shell_connection"):
        return module._shell_connection

    connection_proxy = Connection(module._socket_path)
    cap = json.loads(connection_proxy.get_capabilities())
    if cap["network_api"] == "cliconf":
        module._shell_connection = Connection(module._socket_path)
    #    module._shell_connection.get(command)

    return module._shell_connection


def get_capabilities(module):
    if hasattr(module, "_shell_capabilities"):
        return module._shell_capabilities
    try:
        capabilities = Connection(module._socket_path).get_capabilities()
        module.debug("Capabilities: %s" % to_text(capabilities, errors="surrogate_then_replace"))
    except ConnectionError as exc:
        module.fail_json(msg=to_text(exc, errors="surrogate_then_replace"))
    module._shell_capabilities = json.loads(capabilities)

    return module._shell_capabilities


def to_commands(module, commands):
    if not isinstance(commands, list):
        raise AssertionError("argument must be of type <list>")

    transform = EntityCollection(module, command_spec)
    commands = transform(commands)

    for index, item in enumerate(commands):
        if module.check_mode and not item["command"].startswith("show"):
            module.warn(
                "only show commands are supported when using check mode, not executing `%s`" % item["command"],
            )

    return commands


def to_opnsense_shell_answer(module, commands):
    if not isinstance(commands, dict):
        raise AssertionError("argument must be of type <dict>")
    if not hasattr(commands, "answer"):
        raise AssertionError("argument must have attribute 'answer'")

    # No other modules include the 'opnsense_shell_option' key.
    opnsense_shell_option = module.params.get("opnsense_shell_option")
    opnsense_shell_options = {
        "shell": "8",
        "logout": "0",
        "assign_interfaces": "1",
        "set_interface_ip": "2",
        "reset_root_password": "3",
        "reset_to_factory_defaults": "4",
        "power_off": "5",
        "reboot": "6",
        "ping": "7",
        "pftop": "9",
        "firewall_log": "10",
        "reload_services": "11",
        "update": "12",
        "restore_backup": "13",
    }

    if opnsense_shell_option:
        if opnsense_shell_option in opnsense_shell_options.keys():
            answer = opnsense_shell_options[opnsense_shell_option]
        else:
            # default selection: Shell
            answer = "8"

    commands["answer"] = answer

    return commands


def run_commands(module, commands, check_rc=True):
    # BEGIN DEBUG INSTRUMENTATION
    # import debugpy

    # debugpy.listen(("0.0.0.0", 5678))
    # debugpy.wait_for_client()
    # debugpy.breakpoint()
    # END DEBUG INSTRUMENTATION
    connection = get_connection(module)
    try:
        return connection.run_commands(commands=commands, check_rc=check_rc)
    except ConnectionError as exc:
        module.fail_json(msg=to_text(exc))


def get_config(module, flags=None):
    flags = [] if flags is None else flags

    # Not all modules include the 'passwords' key.
    passwords = module.params.get("passwords", False)
    if passwords:
        cmd = "more system:running-config"
    else:
        cmd = "show running-config "
        cmd += " ".join(flags)
        cmd = cmd.strip()

    try:
        return _DEVICE_CONFIGS[cmd]
    except KeyError:
        conn = get_connection(module)
        out = conn.get(cmd)
        cfg = to_text(out, errors="surrogate_then_replace").strip()
        _DEVICE_CONFIGS[cmd] = cfg
        return cfg


def load_config(module, config):
    try:
        conn = get_connection(module)
        conn.edit_config(config)
    except ConnectionError as exc:
        module.fail_json(msg=to_text(exc))


def get_defaults_flag(module):
    _rc, out, _err = exec_command(module, "show running-config ?")
    out = to_text(out, errors="surrogate_then_replace")

    commands = set()
    for line in out.splitlines():
        if line:
            commands.add(line.strip().split()[0])

    if "all" in commands:
        return "all"
    else:
        return "full"
