from codetocad.adapters.blender.cli.run_blender import run_blender


def install_callback():
    """Installs CodeToCAD as an editable package using pip in the python environment of the consuming application. WARNING: This affects the python environment of the consuming application. TODO: use Virtual Environments."""
    import sys
    import subprocess
    from pathlib import Path
    import sys
    import os
    import subprocess
    import bpy

    from pathlib import Path

    codetocad_path = Path(__file__).parent.parent.parent.absolute()

    target_site = bpy.utils.script_path_user()

    if not codetocad_path.exists():
        raise Exception(f"Could not find CodeToCAD files at {{codetocad_path}}.")

    python = os.path.abspath(sys.executable)

    print(f"{python=}")

    install_command = [
        python,
        "-m",
        "pip",
        "install",
        "-e",
        str(codetocad_path),
        "--target",
        target_site,
    ]

    subprocess.call(install_command)

    subprocess.call([python, "-m", "pip", "list"])

    subprocess.call([sys.executable, "-m", "pip", "list"])
    print("Done!")


def install_codetocad_in_blender():
    """
    Call this function to pip install codetocad in the Blender User Scripts Path.
    """

    run_blender(
        entry_function_or_file=install_callback,
        document_name=None,
        background=True,
        args=[],
        debugger=True,
    )


if __name__ == "__main__":
    install_codetocad_in_blender()
