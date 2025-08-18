import os
import subprocess
import click
from codetocad.adapters.blender.cli.blender_cli import run_blender_process
from codetocad.cli.launcher_args import LauncherArgs


def run_provider(args: LauncherArgs):
    """
    Attempts to run known launchers, and if it fails to do that, runs an unknown process.
    """

    print("LauncherArgs values:")
    print(f"  script_file_path_or_action: {args.script_file_path_or_action}")
    print(f"  launcher: {args.launcher}")
    print(f"  launcher_location: {args.launcher_location}")
    print(f"  background: {args.background}")
    print(f"  document_name: {args.document_name}")
    print(f"  config_file_path: {args.config_file_path}")
    print(f"  debug: {args.debug}")

    # Sample/Dummy/Mock launcher:
    if args.is_sample_launcher():
        click.secho("The sample launcher is not implemented yet.", fg="red")
        return

    launcher_lower = args.launcher.lower()

    # Known launchers:
    if launcher_lower == "blender":
        return run_blender_process(
            blender_path=args.launcher_location or args.launcher,
            document_name=args.document_name,
            script_file_path=args.script_file_path_or_action,
            background=args.background or False,
        )
    # if launcher_lower == "onshape":
    #     return run_onshape(args)

    # Execute an unknown process:
    return subprocess.Popen(args.to_subprocess_args(), env=os.environ)
