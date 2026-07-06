"""Generate images/pendulum.png: release the pendulum example and render it
mid-swing.

    python shoot_pendulum.py
"""
import math
import sys
from pathlib import Path

EXAMPLES_DIR = Path(__file__).resolve().parent.parent
IMAGES_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(EXAMPLES_DIR))
sys.path.insert(0, str(IMAGES_DIR))

from pendulum import build_pendulum
from codetocad_integrations.mujoco import simulate
from _render_common import capture

sim = simulate(build_pendulum(), actuated=False)
sim.set_joint_value("pivot", math.radians(60))
sim.run(0.6)

capture(
    sim,
    sim.data.qpos.copy(),
    str(IMAGES_DIR / "pendulum.png"),
    lookat=[0, 0, 0.35],
    distance=1.05,
    azimuth=130,
    elevation=-12,
)
