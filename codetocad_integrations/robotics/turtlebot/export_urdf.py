"""Export the TurtleBot example's assembly to URDF.

Builds the robot from ``turtlebot_diff_drive.py`` (chassis, two driven
wheels, caster ball), walks its assembly constraints into a kinematic
tree, and writes:

- ``turtlebot.urdf`` next to this script
- every link's mesh as ``meshes/<link>.stl``

The URDF references the meshes relatively (``meshes/...``), so the folder
is self-contained and loads directly in PyBullet, RViz, or any URDF
viewer. The wheel joints have no limits, so they export as ``continuous``
joints.

Run::

    uv run python codetocad_integrations/robotics/turtlebot/export_urdf.py
"""

from __future__ import annotations

import importlib.util
from pathlib import Path

from codetocad.simulation import (
    ensure_binary_stl,
    export_link_meshes,
    extract_links,
)
from codetocad_integrations.pybullet import build_urdf

HERE = Path(__file__).resolve().parent


def load_turtlebot_example():
    """Import the sibling example by file path (this folder is not a
    package)."""
    spec = importlib.util.spec_from_file_location(
        "turtlebot_diff_drive_example", HERE / "turtlebot_diff_drive.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> None:
    chassis, _left_wheel, _right_wheel, _camera = load_turtlebot_example().build_turtlebot()
    links = extract_links(chassis)
    export_link_meshes(links, HERE / "meshes")
    for link in links:
        ensure_binary_stl(link.mesh_path)  # PyBullet/MuJoCo want binary STL
    urdf_path = HERE / "turtlebot.urdf"
    urdf_path.write_text(build_urdf(links, name="turtlebot", mesh_dir="meshes"))
    joints = [link.joint.name for link in links if link.joint is not None]
    print(f"wrote {urdf_path}")
    print(f"wrote {len(links)} meshes to {HERE / 'meshes'}")
    print(f"links:  {[link.name for link in links]}")
    print(f"joints: {joints}")


if __name__ == "__main__":
    main()
