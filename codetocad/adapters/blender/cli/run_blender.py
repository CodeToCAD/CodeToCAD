import os
from typing import Callable
from codetocad.adapters.blender.cli.blender_subprocess import run_blender_process
from codetocad.adapters.blender.cli.config import get_blender_executable_path
from codetocad.cli.config import (
    get_temp_script_path,
)
from codetocad.cli.function_to_file import write_function_code_to_file


RUNNING_IN_BLENDER_ENVIRONMENT_KEY = "RUNNING_IN_BLENDER_ENVIRONMENT"


def _run_blender_file(script_file_path: str):
    """
    This method is a wrapper for`import_codetocad_file()` to import the file inside blender. This method is run inside `_run_blender_callable()`, which writes a temporary file to run inside Blender.
    """
    from codetocad.adapters.blender.blender_actions.file_runner import (
        import_codetocad_file,
    )

    import_codetocad_file(script_file_path)


def _run_blender_callable(
    entry_function: Callable,
    blender_path: str,
    document_name: str | None = None,
    background: bool = True,
    custom_code_to_run_before: str = "",
    custom_code_to_run_after: str = "",
    debugger: bool = False,
    args: list = [],
    kwargs: dict = {},
):
    """
    Runs a function using the configured Blender executable path.
    The function is written to a temporary file at `config.get_temp_script_path()` and executed.

    Call `set_blender_executable_path("/Applications/Blender.app/Contents/MacOS/Blender") && install_codetocad_in_blender()` before using this function.
    """

    def add_user_script_dir_to_path():
        """Eval this inside the Blender environment, after `install_codetocad_in_blender()` and whenever Blender is restarted."""
        return """
import sys
import bpy
sys.path.append(bpy.utils.script_path_user()) #type: ignore

from codetocad.adapters.blender import *
"""

    def add_running_in_blender_env_var():
        return f"""
from codetocad.adapters.blender.cli.run_blender import set_running_in_blender_environment_var

set_running_in_blender_environment_var()
"""

    def add_debugger_code():
        return """
from codetocad.adapters.blender.blender_actions.console import start_debugger, stop_debugger

start_debugger(wait_to_connect=True)
"""

    def check_install_and_install():
        return f"""
try:
    import codetocad
    import click
except:
    from codetocad.adapters.blender.cli.install_codetocad_in_blender import (
install_codetocad_in_blender
)
    print("CodeToCAD is not installed, installing it now!")
    install_codetocad_in_blender()
    """

    custom_code_to_run_before = f"""
{add_user_script_dir_to_path()}
{add_running_in_blender_env_var()}
{check_install_and_install()}

{custom_code_to_run_before}
{add_debugger_code() if debugger else ""}
"""

    if debugger:
        custom_code_to_run_after += f"""
stop_debugger()
        """

    script_path = str(get_temp_script_path())
    write_function_code_to_file(
        func=entry_function,
        output_path=script_path,
        prepend_code=custom_code_to_run_before,
        append_code=custom_code_to_run_after,
        args=args,
        kwargs=kwargs,
    )

    return run_blender_process(
        blender_path=blender_path,
        document_name=document_name,
        script_file_path=script_path,
        background=background,
    )


def _check_if_in_blender():
    try:
        return (
            RUNNING_IN_BLENDER_ENVIRONMENT_KEY in os.environ
            and os.environ[RUNNING_IN_BLENDER_ENVIRONMENT_KEY]
        )
    except:
        return False


def set_running_in_blender_environment_var():
    os.environ[RUNNING_IN_BLENDER_ENVIRONMENT_KEY] = "1"


def run_blender(
    entry_function_or_file: Callable | str,
    document_name: str | None = None,
    background: bool = True,
    custom_code_to_run_before: str = "",
    custom_code_to_run_after: str = "",
    debugger: bool = False,
    *,
    args: list = [],
    kwargs: dict = {},
):
    """
    Runs a function using the configured Blender executable path.

    Call `set_blender_executable_path("/Applications/Blender.app/Contents/MacOS/Blender") && install_codetocad_in_blender()` before using this function.
    """
    blender_path = get_blender_executable_path()

    if not blender_path:
        raise ValueError(
            "Blender executable path is not set. Please set it using set_blender_executable_path()."
        )

    entry_function = entry_function_or_file

    if _check_if_in_blender():
        from codetocad.adapters.blender.blender_actions.console import write_to_console

        # We are already in Blender, so we can just run the function:
        write_to_console("Warning: run_blender() was called inside Blender.")
        if isinstance(entry_function_or_file, str):
            raise ValueError("Cannot run a file inside Blender.")
        return entry_function_or_file(*args, **kwargs)

    if isinstance(entry_function, str):
        args = [entry_function]
        entry_function = _run_blender_file

    return _run_blender_callable(
        entry_function=entry_function,
        args=args,
        blender_path=blender_path,
        document_name=document_name,
        background=background,
        custom_code_to_run_before=custom_code_to_run_before,
        custom_code_to_run_after=custom_code_to_run_after,
        debugger=debugger,
    ).wait()
