"""Generate images/arm_6dof.png: pose the 6-DOF arm example mid-motion and
render it offscreen.

    python shoot_arm_6dof.py

Requires the mujoco + build123d extras (this repo's .venv-sim works well).
"""
import sys
from pathlib import Path

EXAMPLES_DIR = Path(__file__).resolve().parent.parent
IMAGES_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(EXAMPLES_DIR))
sys.path.insert(0, str(IMAGES_DIR))

from arm_6dof import build_arm
from codetocad import Lighting
from codetocad_integrations.mujoco import simulate
from _render_common import capture

arm = build_arm()
sim = simulate(
    arm, lighting=[Lighting(light_type="directional", position=(1.0, 1.0, 2.0))]
)
names = sim.joint_names
goals = (0.5, 0.4, -0.6, 0.8, 0.5, -1.0)
for name, goal in zip(names, goals):
    sim.set_joint_target(name, goal)
sim.run(5.0)

capture(
    sim,
    sim.data.qpos.copy(),
    str(IMAGES_DIR / "arm_6dof.png"),
    lookat=[0, 0, 0.28],
    distance=1.1,
    azimuth=135,
    elevation=-18,
)
