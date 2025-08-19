from codetocad.adapters.blender.cli.run_blender import run_blender


def pip_install_codetocad_as_string(target_site_expression: str | None):
    """Installs CodeToCAD as an editable package using pip in the python environment of the consuming application. WARNING: This affects the python environment of the consuming application. TODO: use Virtual Environments."""
    from pathlib import Path

    pipe_stdout = ""
    # pipe_stdout = "stdout=subprocess.PIPE, stderr=subprocess.PIPE"

    pip_instal_string = f'subprocess.call([python, "-m", "pip", "install", "-e", str(codetocad_path)], {pipe_stdout})'
    if target_site_expression:
        pip_instal_string = f'subprocess.call([python, "-m", "pip", "install", "-e", str(codetocad_path), "--target", {target_site_expression}],  {pipe_stdout})'

    return f"""
from pathlib import Path
import sys
import os
import subprocess
codetocad_path = Path("{Path(__file__).parent.parent.parent.absolute()}")

if not codetocad_path.exists():
    raise Exception(
        f"Could not find CodeToCAD files at {{codetocad_path}}."
    )

python = os.path.abspath(sys.executable)

print(f"{{python=}}")

{pip_instal_string}

subprocess.call([python, "-m", "pip", "list"], {pipe_stdout})

"""


def install_codetocad_in_blender():
    """
    Call this function to pip install codetocad in the Blender User Scripts Path.
    """

    def install():
        import sys
        import subprocess

        subprocess.call([sys.executable, "-m", "pip", "list"])
        print("Done!")

    run_blender(
        entry_function_or_file=install,
        document_name=None,
        background=True,
        custom_code_to_run_before=f"""
import bpy
{pip_install_codetocad_as_string('bpy.utils.script_path_user()')}
        """,
    )


if __name__ == "__main__":
    install_codetocad_in_blender()
