import runpy
from codetocad.launchers.launcher_args import LauncherArgs


def run_with_providers_sample(launcher_args: LauncherArgs):
    """
    Launches the script with the codetocad.providers_sample module.
    """
    return runpy.run_path(launcher_args.script_file_path, run_name="__main__")
