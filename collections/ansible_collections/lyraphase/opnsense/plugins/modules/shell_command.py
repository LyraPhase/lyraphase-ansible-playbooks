#!/usr/bin/python
#
# Copyright: Ansible Project
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

import time

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.six import string_types
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.parsing import (
    Conditional,
)
from ansible_collections.lyraphase.opnsense.plugins.module_utils.network.opnsense.shell import (
    check_args,
    run_commands,
    shell_argument_spec,
)


__metaclass__ = type


DOCUMENTATION = """
module: shell_command
author: James Cuzella (@trinitronx)
short_description: Run arbitrary commands on OPNsense devices
description:
- Sends arbitrary commands to an OPNsense host and returns the results read
  from the device.
  The C(shell_command) module includes an argument that will cause the module
  to wait for a specific condition before returning or timing out if the
  condition is not met.
version_added: 1.0.0
extends_documentation_fragment:
- lyraphase.opnsense.become
options:
  commands:
    description:
    - List of commands to send to the remote device over the configured
      provider.  The resulting output from the command is returned. If the
      I(wait_for) argument is provided, the module is not returned until the
      condition is satisfied or the number of retires as expired.
    required: true
    type: list
    elements: str
  wait_for:
    description:
    - List of conditions to evaluate against the output of the command. The
      task will wait for each condition to be true before moving forward. If
      the conditional is not true within the configured number of retries, the
      task fails. See examples.
    aliases:
    - waitfor
    type: list
    elements: str
  match:
    description:
    - The I(match) argument is used in conjunction with the I(wait_for)
      argument to specify the match policy.  Valid values are C(all) or
      C(any).  If the value is set to C(all) then all conditionals in the
      C(wait_for) must be satisfied.  If the value is set to C(any) then only
      one of the values must be satisfied.
    default: all
    choices:
    - any
    - all
    type: str
  retries:
    description:
    - Specifies the number of retries a command should by tried before it is
      considered failed. The command is run on the target device every retry
      and evaluated against the I(wait_for) conditions.
    default: 10
    type: int
  interval:
    description:
    - Configures the interval in seconds to wait between retries of the
      command. If the command does not pass the specified conditions, the
      interval indicates how long to wait before trying the command again.
    default: 1
    type: int
notes:
- When processing wait_for, each commands' output is stored as an element of
  the I(result) array.  The allowed operators for conditional evaluation are
  I(eq), I(==), I(neq), I(ne), I(!=), I(gt), I(>), I(ge), I(>=), I(lt), I(<),
  I(le), I(<=), I(contains), I(matches).  Operators can be prefaced by I(not)
  to negate their meaning.  The I(contains) operator searches for a substring
  match (like the Python I(in) operator).  The I(matches) operator searches
  using a regex search operation.
"""

EXAMPLES = """
- name: Show the OPNsense version
  lyraphase.opnsense.shell_command:
    commands:
      - opnsense-version

- name: Show FreeBSD version
  lyraphase.opnsense.shell_command:
    commands:
      - freebsd-version

- name: Show OPNsense log types
  become: true
  lyraphase.opnsense.shell_command:
    commands:
      - opnsense-log -l

- name: Show OPNsense routing logs
  become: true
  lyraphase.opnsense.shell_command:
    commands:
      - opnsense-log routing

- name: Show memory usage
  lyraphase.opnsense.shell_command:
    commands:
      - sysctl hw | egrep 'hw.(phys|user|real)'

- name: Send repeat pings and wait for the result to pass 100%
  lyraphase.opnsense.shell_command:
    become: true
    commands:
      - ping -c 20 -s 350 8.8.8.8
    wait_for:
      - result[-2] contains '0.0% packet loss'
    retries: 2

- name: Send ICMP ping sweep using min size 1472, max size 8972, increment 100
  lyraphase.opnsense.shell_command:
    become: true
    commands:
      - ping -g 1472 -h 10 -G 8972 -c 1 192.168.1.100

- name: >
    Send ICMP ping sweep to detect jumbo frames support
    using min size 8970, max size 8972, increment 1
    (8972 + 8 byte packet header = 8980 max size)
  lyraphase.opnsense.shell_command:
    become: true
    commands:
      - ping -g 8970 -h 1 -G 8972 -c 1 192.168.1.100
"""

RETURN = """
stdout:
  description: the set of responses from the commands
  returned: always
  type: list
  sample: ['...', '...']

stdout_lines:
  description: The value of stdout split into a list
  returned: always
  type: list
  sample: [['...', '...'], ['...'], ['...']]

failed_conditions:
  description: the conditionals that failed
  returned: failed
  type: list
  sample: ['...', '...']
"""


def to_lines(stdout):
    for item in stdout:
        if isinstance(item, string_types):
            item = str(item).split("\n")
        yield item


def main():
    spec = {
        # { command: <str>, prompt: <str>, response: <str> }
        # "become": {"type": "bool", "default": False},
        "commands": {"type": "list", "required": True, "elements": "str"},
        "wait_for": {"type": "list", "aliases": ["waitfor"], "elements": "str"},
        "match": {"default": "all", "choices": ["all", "any"], "type": "str"},
        "retries": {"default": 10, "type": "int"},
        "interval": {"default": 1, "type": "int"},
    }

    spec.update(shell_argument_spec)

    module = AnsibleModule(argument_spec=spec, supports_check_mode=True)
    check_args(module)

    result = {"changed": False}

    wait_for = module.params["wait_for"] or []
    conditionals = [Conditional(c) for c in wait_for]

    commands = module.params["commands"]
    retries = module.params["retries"]
    interval = module.params["interval"]
    match = module.params["match"]
    # become = module.params["become"]

    # TODO: Figure out where this needs to go... AnsibleModule is already
    # running inside the AnsiballZ context, so there is no "connection"...
    # Except, network_cli plugins still do have a network connection, so which
    # context is that in?

    # This did not work
    # if become:
    #     connection = module.get_connection()
    #     connection.on_become()
    #     connection._terminal.on_become(module, passwd=module.params.get("become_password"))

    while retries > 0:
        responses = run_commands(module, commands)

        for item in conditionals:
            if item(responses):
                if match == "any":
                    conditionals = []
                    break
                conditionals.remove(item)

        if not conditionals:
            break

        time.sleep(interval)
        retries -= 1

    if conditionals:
        failed_conditions = [item.raw for item in conditionals]
        msg = "One or more conditional statements have not be satisfied"
        module.fail_json(msg=msg, failed_conditions=failed_conditions)

    result.update(
        {
            "changed": False,
            "stdout": responses,
            "stdout_lines": list(to_lines(responses)),
        },
    )

    module.exit_json(**result)


if __name__ == "__main__":
    main()
