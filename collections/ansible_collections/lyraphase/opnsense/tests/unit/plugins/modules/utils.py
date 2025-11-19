from __future__ import absolute_import, division, print_function


__metaclass__ = type
import json
import sys

from unittest import TestCase
from unittest.mock import patch

from ansible.module_utils import basic


try:
    from ansible.module_utils.common.text.converters import to_bytes, to_text
except ImportError:
    from ansible.module_utils._text import to_bytes

VERBOSITY = 4
CONSOLE = sys.stderr


import inspect


def debug_global_frame():
    frame = inspect.currentframe()
    # Go back to the top-level frame
    while frame.f_back:
        frame = frame.f_back
    # The code object is stored in f_code
    return frame.f_code


def debug_stacktrace():
    A = [inspect.getframeinfo(f[0]) for f in inspect.stack()]
    log("%s:%s" % (A[0].filename, A[0].lineno), 4)
    # log("traceback structure fields: %s" % "\n".join([x for x in filter(lambda s: s[0] != "_", dir(A[0]))]), 4)
    for F in A:
        log("\t%s:%s\t%s\t%s" % (F.filename, F.lineno, F.function, F.positions), 4)

    # for f in inspect.stack():
    # F = inspect.getframeinfo(f[0])
    # log("-" + F.filename + F.lineno + "\t" + F.code_context[0].strip(), 4)
    # The code object is stored in f_code
    # log("Stacktrace: %s" % to_text(tb, errors="surrogate_then_replace"), 4)


def log(message, verbosity=0):  # type: (str, int) -> None
    """Log a message to the console if the verbosity is high enough."""
    if verbosity > VERBOSITY:
        return

    print(message, file=CONSOLE)
    CONSOLE.flush()
    with open("/tmp/ansible-opnsense-test.log", "a") as f:
        f.write("%s\n" % message)
        f.flush()


def set_module_args(args):
    if "_ansible_remote_tmp" not in args:
        args["_ansible_remote_tmp"] = "/tmp"
    if "_ansible_keep_remote_files" not in args:
        args["_ansible_keep_remote_files"] = False

    args = json.dumps({"ANSIBLE_MODULE_ARGS": args})
    log("Module args: %s" % to_text(args, errors="surrogate_then_replace"), 4)
    debug_stacktrace()
    basic._ANSIBLE_ARGS = to_bytes(args)


class AnsibleExitJson(Exception):
    pass


class AnsibleFailJson(Exception):
    pass


def exit_json(*args, **kwargs):
    if "changed" not in kwargs:
        kwargs["changed"] = False
    raise AnsibleExitJson(kwargs)


def fail_json(*args, **kwargs):
    kwargs["failed"] = True
    raise AnsibleFailJson(kwargs)


class ModuleTestCase(TestCase):
    def setUp(self):
        self.mock_module = patch.multiple(
            basic.AnsibleModule,
            exit_json=exit_json,
            fail_json=fail_json,
        )
        self.mock_module.start()
        self.mock_sleep = patch("time.sleep")
        self.mock_sleep.start()
        set_module_args({})
        log("Module: %s" % to_text(basic, errors="surrogate_then_replace"), 4)
        self.addCleanup(self.mock_module.stop)
        self.addCleanup(self.mock_sleep.stop)

    def log(self, msg, verbosity=0):
        log(msg, verbosity)
