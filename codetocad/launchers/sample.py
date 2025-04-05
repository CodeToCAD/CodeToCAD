import os
import sys
import subprocess
from pathlib import Path
import runpy

from codetocad.launchers.launcher_args import LauncherArgs
from providers.sample import register


def run_with_sample(launcher_args: LauncherArgs):
    """
    Launches the script with the providers.sample module.
    """
    register.register()

    filepath = launcher_args.script_file_path_or_action

    # Add script directory to path to make some scripts work
    directory = str(Path(filepath).parent)
    sys.path.append(directory)

    python = os.path.abspath(sys.executable)

    if launcher_args.debug:
        return subprocess.call(
            [python, "-m", "debugpy", "--listen", "5678", "--wait-for-client", filepath]
        )

    return runpy.run_path(filepath, run_name="__main__")
