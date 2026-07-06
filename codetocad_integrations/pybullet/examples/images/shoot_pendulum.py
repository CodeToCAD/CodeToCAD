"""Generate images/pendulum.png: release the pendulum example and screenshot
it mid-swing.

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
from codetocad_integrations.pybullet import simulate
from _render_common import capture

sim = simulate(build_pendulum(), gui=False)
sim.set_joint_value("pivot", math.radians(60))
sim.run(1.2)

capture(
    sim,
    str(IMAGES_DIR / "pendulum.png"),
    eye=[0.9, 0.95, 0.55],
    target=[0, 0, 0.35],
)
sim.close()
