from codetocad.launchers.blender import run_blender_process
from codetocad.launchers.launcher_args import LauncherArgs
from codetocad.launchers.unknown_launcher import run_unknown_process


def execute_launcher():
    args = LauncherArgs.from_cli_args()

    if args.is_sample_launcher():
        print("Running script with the provider_sample.")
        return

    launcher_lower = args.launcher.lower()

    if launcher_lower == "blender":
        return run_blender_process(args)

    run_unknown_process(args)


if __name__ == "__main__":
    execute_launcher()
