"""Relaunch CodeToCAD scripts inside Blender's bundled Python."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

try:
    import bpy  # noqa: F401 - only available inside Blender

    INSIDE_BLENDER = True
except ImportError:
    INSIDE_BLENDER = False


def _blender_executable() -> str:
    return os.environ.get("CODETOCAD_BLENDER", "blender")


def _packages_root() -> Path:
    """Directory containing the codetocad and codetocad_integrations
    packages, to put on Blender's PYTHONPATH."""
    import codetocad

    return Path(codetocad.__file__).resolve().parent.parent


def blender_command(script: str | Path) -> tuple[list[str], dict[str, str]]:
    """The (command, env) to run ``script`` headless inside Blender."""
    root = str(_packages_root())
    env = os.environ.copy()
    env["PYTHONPATH"] = os.pathsep.join(
        [root] + ([env["PYTHONPATH"]] if env.get("PYTHONPATH") else [])
    )
    command = [
        _blender_executable(),
        "--background",
        "--factory-startup",
        "--python-exit-code",
        "1",
        # Put this repo's packages ahead of anything installed in Blender's
        # own site-packages (e.g. another codetocad checkout).
        "--python-expr",
        f"import sys; sys.path.insert(0, {root!r})",
        "--python",
        str(script),
    ]
    return command, env


def run_in_blender(script: str | Path) -> int:
    """Run a python script headless inside Blender; returns the exit code."""
    command, env = blender_command(script)
    return subprocess.run(command, env=env).returncode


def reset_scene() -> None:
    """Start from an empty scene (no default cube/camera/light)."""
    import bpy

    bpy.ops.wm.read_factory_settings(use_empty=True)


def ensure_blender(reset: bool = True) -> None:
    """Make sure the current script is running inside Blender.

    Inside Blender: optionally reset to an empty scene and return.
    Outside: relaunch the current script with ``blender --background`` and
    exit with its return code.
    """
    if INSIDE_BLENDER:
        if reset:
            reset_scene()
        return
    script = Path(sys.argv[0]).resolve()
    if not script.exists():
        raise RuntimeError(
            "ensure_blender() could not determine the current script path; "
            "run your design as a file (codetocad my_design.py)"
        )
    sys.exit(run_in_blender(script))
