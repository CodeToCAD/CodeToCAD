import os
import subprocess
import sys
import click
from codetocad.cli.launcher_args import LauncherArgs
from codetocad.cli.run_provider import run_provider

python = os.path.abspath(sys.executable)


def codetocad_cli():
    cli = click.Group()

    # Version command
    @click.command("version")
    def version_cmd():
        click.secho("Displaying the current version of CodeToCAD:", fg="green")
        subprocess.call([python, "-m", "pip", "show", "codetocad"])

    # Update command
    @click.command("update")
    def update_cmd():
        click.secho("Updating codetocad:", fg="green")
        subprocess.call([python, "-m", "pip", "install", "-U", "codetocad"])

    # Uninstall command
    @click.command("uninstall")
    def uninstall_cmd():
        click.secho("Uninstalling codetocad from cli:", fg="green")
        subprocess.call([python, "-m", "pip", "uninstall", "codetocad"])

    # Run command
    @click.command("run")
    @click.argument("script_file_path", type=str)
    @click.argument(
        "launcher", required=False, default=LauncherArgs.get_sample_launcher_name()
    )
    @click.option("--launcher_location", type=str, help="Path or URL of the launcher")
    @click.option(
        "--background", is_flag=True, help="Run the process in the background"
    )
    @click.option(
        "--document_name", type=str, help="Document name or output file destination"
    )
    @click.option("--config_file_path", type=str, help="Path to a config file")
    @click.option("--debug", is_flag=True, help="Enable debug mode")
    def run_cmd(
        script_file_path,
        launcher,
        launcher_location,
        background,
        document_name,
        config_file_path,
        debug,
    ):
        args = LauncherArgs(
            script_file_path_or_action=script_file_path,
            launcher=launcher,
            launcher_location=launcher_location,
            background=background,
            document_name=document_name,
            config_file_path=config_file_path,
            debug=debug,
        )

        run_provider(args)

    cli.add_command(version_cmd)
    cli.add_command(update_cmd)
    cli.add_command(uninstall_cmd)
    cli.add_command(run_cmd)

    cli(sys.argv[1:])


if __name__ == "__main__":
    codetocad_cli()
