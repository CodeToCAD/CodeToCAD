"""Generate images/arm_6dof.png: pose the 6-DOF arm example mid-motion and
screenshot it headlessly.

    python shoot_arm_6dof.py

Requires the pybullet + build123d extras (a venv with pybullet built, e.g.
this repo's .venv-sim, works well since pybullet needs a C build step).
"""
import sys
from pathlib import Path

EXAMPLES_DIR = Path(__file__).resolve().parent.parent
IMAGES_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(EXAMPLES_DIR))
sys.path.insert(0, str(IMAGES_DIR))

from arm_6dof import build_arm
from codetocad import Lighting
from codetocad_integrations.pybullet import simulate
from _render_common import capture

arm = build_arm()
sim = simulate(
    arm, gui=False, lighting=[Lighting(light_type="point", position=(1.0, 1.0, 2.0))]
)
names = sim.joint_names
goals = (0.5, 0.4, -0.6, 0.8, 0.5, -1.0)
for name, goal in zip(names, goals):
    sim.set_joint_target(name, goal)
sim.run(3.0)

capture(
    sim,
    str(IMAGES_DIR / "arm_6dof.png"),
    eye=[0.62, 0.62, 0.55],
    target=[0, 0, 0.28],
    fov=45,
)
sim.close()
