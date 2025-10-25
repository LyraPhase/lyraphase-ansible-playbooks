#!/usr/bin/env python2
import os
import sys


def which(cmd):
    """Return the full path to *cmd* if it is found in the PATH, else None."""
    # If the command already contains a directory separator, just test it.
    if os.path.dirname(cmd):
        return cmd if os.access(cmd, os.X_OK) else None

    # Get the PATH environment variable and split it into directories.
    path_dirs = os.environ.get("PATH", "").split(os.pathsep)

    for directory in path_dirs:
        directory = directory.strip('"')
        full_path = os.path.join(directory, cmd)
        if os.access(full_path, os.X_OK):
            return full_path
    return None


env = os.environ
script = "/output/scripts/introspect.py3.py"
python = "python3.9"
py_bin = which(python)
args = [py_bin, script]
args.extend(sys.argv)
args.remove("/output/scripts/introspect.py")
if os.access(script, os.R_OK):
    os.execve(py_bin, args, env)
else:
    sys.stderr.write("Error: Could not execute script: %s" % script)
