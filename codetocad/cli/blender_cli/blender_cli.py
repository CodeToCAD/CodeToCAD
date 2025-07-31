import os
import subprocess
from typing import Callable

from codetocad.cli.add_to_path import pip_install_codetocad_as_string
from codetocad.cli.config import (
    ConfigProvider,
    get_temp_script_path,
    read_config,
    write_config,
)
from codetocad.cli.function_to_file import write_function_code_to_file


def build_blender_subprocess_args(
    blender_path: str,
    document_name: str | None,
    script_file_path: str,
    background: bool,
):
    """
    builds a path like:
    blender --python /path/to/your_script.py
    blender --background --python /path/to/your_script.py
    blender myscene.blend --background -- --codetocad $(pwd)/yourScript.py

    from LauncherArgs

    References https://docs.blender.org/manual/en/latest/advanced/command_line/arguments.html#python-options
    """

    args = [blender_path]

    if document_name:
        # todo: check for the .blend suffix
        args.append(document_name)

    if background:
        args.append("--background")

    args += ["--python", script_file_path]

    return args


def run_blender_process(
    blender_path: str,
    document_name: str | None,
    script_file_path: str,
    background: bool,
):
    """
    Attempts to launch blender and run the provided script path.
    The CodeToCAD Blender Addon must be installed for this to work.
    """
    return subprocess.Popen(
        build_blender_subprocess_args(
            blender_path=blender_path,
            document_name=document_name,
            script_file_path=script_file_path,
            background=background,
        ),
        env=os.environ,
    )


def set_blender_executable_path(blender_path: str):
    """
    Sets the Blender executable path in the configuration file.
    """
    if not os.path.exists(blender_path):
        raise FileNotFoundError(f"Blender executable not found at {blender_path}")

    blender_config = ConfigProvider(name="blender", path=blender_path)

    config = read_config()

    if "blender" in config.providers:
        blender_config = config.providers["blender"]

    blender_config.path = blender_path

    config.providers["blender"] = blender_config

    write_config(config)


def get_blender_executable_path() -> str | None:
    """
    Retrieves the Blender executable path from the configuration file.
    """
    config = read_config()
    blender_config = config.providers.get("blender", None)
    return blender_config.path if blender_config else None


def install_codetocad_in_blender():
    """
    Call this function to pip install codetocad in the Blender User Scripts Path.
    Using `run()` will call `add_user_script_dir_to_path()` so that codetocad  and its dependencies can be imported inside Blender.
    """

    def install():
        import sys
        import subprocess

        subprocess.call([sys.executable, "-m", "pip", "list"])
        print("Done!")

    run(
        entry_function=install,
        document_name=None,
        background=True,
        custom_code_to_run_before=f"""
import bpy
{pip_install_codetocad_as_string('bpy.utils.script_path_user()')}
        """,
        custom_code_to_run_after=add_user_script_dir_to_path(),
    )


def add_user_script_dir_to_path():
    """Eval this inside the Blender environment, after `install_codetocad_in_blender()` and whenever Blender is restarted."""
    return """
import sys
import bpy
sys.path.append(bpy.utils.script_path_user()) #type: ignore
"""


def run(
    entry_function: Callable,
    document_name: str | None = None,
    background: bool = True,
    custom_code_to_run_before: str = "",
    custom_code_to_run_after: str = "",
):
    """
    Runs a function using the configured Blender executable path.
    """
    blender_path = get_blender_executable_path()

    if not blender_path:
        raise ValueError(
            "Blender executable path is not set. Please set it using set_blender_executable_path()."
        )

    custom_code_to_run_before = f"""
{add_user_script_dir_to_path()}
{custom_code_to_run_before}
    """

    script_path = str(get_temp_script_path())
    write_function_code_to_file(
        func=entry_function,
        output_path=script_path,
        prepend_code=custom_code_to_run_before,
        append_code=custom_code_to_run_after,
    )

    return run_blender_process(
        blender_path=blender_path,
        document_name=document_name,
        script_file_path=script_path,
        background=background,
    )
