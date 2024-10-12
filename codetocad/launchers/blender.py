import os
import subprocess
from codetocad.launchers.launcher_args import LauncherArgs


def build_blender_subprocess_args(launcher_args: LauncherArgs):
    """
    builds a path like:
    blender myscene.blend --background -- --codetocad $(pwd)/yourScript.py

    from LauncherArgs
    """

    args = [launcher_args.launcher_location or launcher_args.launcher]

    if launcher_args.document_name:
        # todo: check for the .blend suffix
        args.append(launcher_args.document_name)

    if launcher_args.background:
        args.append("--background")

    args += ["--", "--codetocad", launcher_args.script_file_path_or_action]

    return args


def run_blender_process(launcher_args: LauncherArgs):
    """
    Attempts to launch blender and run the provided script path.
    The CodeToCAD Blender Addon must be installed for this to work.
    """
    return subprocess.Popen(
        build_blender_subprocess_args(launcher_args), env=os.environ
    )
