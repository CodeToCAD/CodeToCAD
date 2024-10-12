import runpy
from codetocad.launchers.launcher_args import LauncherArgs

from providers.sample import register


def run_with_sample(launcher_args: LauncherArgs):
    """
    Launches the script with the providers.sample module.
    """
    register.register()
    return runpy.run_path(launcher_args.script_file_path_or_action, run_name="__main__")
