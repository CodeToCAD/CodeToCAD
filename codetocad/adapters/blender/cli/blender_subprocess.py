import os
import subprocess


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
    blender myscene.blend --background -- --codetocad custom_args

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
    NOTE: In most cases, you want to use `run_blender()` instead of this function.
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
