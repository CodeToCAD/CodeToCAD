"""Generate images/turtlebot_drive.gif: drive the turtlebot forward and
record the MuJoCo viewport to an animated GIF.

    python shoot_turtlebot.py

Requires the mujoco extra (this repo's .venv-sim works well).
"""
import sys
from pathlib import Path

EXAMPLE_DIR = Path(__file__).resolve().parent.parent
IMAGES_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(EXAMPLE_DIR))
sys.path.insert(0, str(IMAGES_DIR))

from turtlebot_diff_drive import MOTOR_NO_LOAD_RPM, build_turtlebot, make_simulation

from _render_common import record_gif

chassis, left_wheel, right_wheel, camera = build_turtlebot()
sim = make_simulation(chassis)

record_gif(
    sim,
    str(IMAGES_DIR / "turtlebot_drive.gif"),
    duration_seconds=3.5,
    fps=15,
    # Fixed side-on shot (rather than a robot-tracking camera) so the
    # forward drive reads as left-to-right motion across the frame.
    lookat=[0.19, 0, 0.05],
    distance=0.8,
    azimuth=90,
    elevation=-15,
    joint_velocities_rpm={
        "left_axle": 0.55 * MOTOR_NO_LOAD_RPM,
        "right_axle": 0.55 * MOTOR_NO_LOAD_RPM,
    },
)
