"""Generate images/double_pendulum.png: release the double pendulum example
and screenshot it mid-swing.

    python shoot_double_pendulum.py
"""
import math
import sys
from pathlib import Path

EXAMPLES_DIR = Path(__file__).resolve().parent.parent
IMAGES_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(EXAMPLES_DIR))
sys.path.insert(0, str(IMAGES_DIR))

from double_pendulum import build_double_pendulum
from codetocad_integrations.pybullet import simulate
from _render_common import capture

sim = simulate(build_double_pendulum(), gui=False)
sim.set_joint_value("pivot1", math.radians(90))
sim.set_joint_value("pivot2", 0.0)
sim.run(0.9)

capture(
    sim,
    str(IMAGES_DIR / "double_pendulum.png"),
    eye=[1.1, 1.15, 0.65],
    target=[0, 0, 0.4],
)
sim.close()
