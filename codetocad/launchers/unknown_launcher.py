import os
import subprocess
from codetocad.launchers.launcher_args import LauncherArgs


def run_unknown_process(launcher_args: LauncherArgs):
    return subprocess.Popen(launcher_args.to_subprocess_args(), env=os.environ)
