"""Generate images/double_pendulum.gif: release the double pendulum example
and record its chaotic swing.

    python shoot_double_pendulum_gif.py
"""
import math
import sys
from pathlib import Path

EXAMPLES_DIR = Path(__file__).resolve().parent.parent
IMAGES_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(EXAMPLES_DIR))
sys.path.insert(0, str(IMAGES_DIR))

from double_pendulum import build_double_pendulum

from codetocad_integrations.mujoco import simulate

from _render_common import record_gif

sim = simulate(build_double_pendulum(), actuated=False)
sim.set_joint_value("pivot1", math.radians(90))
sim.set_joint_value("pivot2", 0.0)

record_gif(
    sim,
    str(IMAGES_DIR / "double_pendulum.gif"),
    duration_seconds=3.0,
    fps=20,
    lookat=[0, 0, 0.4],
    distance=1.2,
    azimuth=130,
    elevation=-10,
)
