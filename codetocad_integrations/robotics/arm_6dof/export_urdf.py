"""Export the 6-DOF arm example's assembly to URDF.

Builds the arm from ``codetocad_integrations/mujoco/examples/arm_6dof.py``
(the Build123D model with clevis/pin joints and the parallel-jaw gripper),
walks its assembly constraints into a kinematic tree, and writes:

- ``arm_6dof.urdf`` next to this script
- every link's mesh as ``meshes/<link>.stl``

The URDF references the meshes relatively (``meshes/...``), so the folder
is self-contained and loads directly in PyBullet, RViz, or any URDF
viewer.

Run::

    uv run python codetocad_integrations/robotics/arm_6dof/export_urdf.py
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
ARM_EXAMPLE = HERE.parents[1] / "mujoco" / "examples" / "arm_6dof.py"


def load_arm_example():
    """Import the arm example by file path (the examples folder is not a
    package)."""
    spec = importlib.util.spec_from_file_location("arm_6dof_example", ARM_EXAMPLE)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> None:
    arm = load_arm_example().build_arm()
    links = extract_links(arm)
    export_link_meshes(links, HERE / "meshes")
    for link in links:
        ensure_binary_stl(link.mesh_path)  # PyBullet/MuJoCo want binary STL
    urdf_path = HERE / "arm_6dof.urdf"
    urdf_path.write_text(build_urdf(links, name="arm_6dof", mesh_dir="meshes"))
    joints = [link.joint.name for link in links if link.joint is not None]
    print(f"wrote {urdf_path}")
    print(f"wrote {len(links)} meshes to {HERE / 'meshes'}")
    print(f"links:  {[link.name for link in links]}")
    print(f"joints: {joints}")


if __name__ == "__main__":
    main()
