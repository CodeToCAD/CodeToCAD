"""MuJoCo integration: simulate CodeToCAD assemblies.

``simulate(part)`` walks the assembly constraints (fixed/revolute/prismatic)
recorded on a root Part3D, exports every part's mesh as STL, generates an
MJCF model and loads it into MuJoCo. Model in Build123D or Blender and
import into simulation right away.

Note: on macOS the interactive viewer must run under ``mjpython`` (ships
with the mujoco package); headless simulation works with any Python.
"""

from .simulation import MujocoSimulation, build_mjcf, simulate

__all__ = ["simulate", "MujocoSimulation", "build_mjcf"]
