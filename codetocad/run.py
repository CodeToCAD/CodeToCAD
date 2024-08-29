from codetocad.launchers.blender import run_blender_process
from codetocad.launchers.launcher_args import LauncherArgs
from codetocad.launchers.sample import run_with_sample
from codetocad.launchers.unknown_launcher import run_unknown_process


def execute_launcher():
    """
    Builds a LauncherArgs instance from cli args, then attempts to run known launchers, and if it fails to do that, runs an unknown process.
    """
    args = LauncherArgs.from_cli_args()

    # Sample/Dummy/Mock launcher:
    if args.is_sample_launcher():
        print(
            """Running script with the sample provider. 
            NOTE: This will show the execution path, but will not generate any models. To generate models, you should run CodeToCAD in a modeling software, e.g. Blender or Fusion360. 
            See https://github.com/CodeToCAD/CodeToCAD/README.md for more information.
            """
        )
        run_with_sample(args)
        return

    launcher_lower = args.launcher.lower()

    # Known launchers:
    if launcher_lower == "blender":
        return run_blender_process(args)

    # Execute an unknown process:
    run_unknown_process(args)


if __name__ == "__main__":
    execute_launcher()
