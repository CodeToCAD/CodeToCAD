"""Generate images/arm_6dof.png: the 6-DOF arm holding the picked-up cube,
rendered offscreen.

    python shoot_arm_6dof.py

Requires the mujoco + build123d extras (this repo's .venv-sim works well).
"""
import sys
from pathlib import Path

EXAMPLES_DIR = Path(__file__).resolve().parent.parent
IMAGES_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(EXAMPLES_DIR))
sys.path.insert(0, str(IMAGES_DIR))

from arm_6dof import build_arm, build_pick_cube, run_pick
from codetocad import Lighting
from codetocad_integrations.mujoco import simulate
from _render_common import capture

sim = simulate(
    build_arm(),
    ground_plane=True,
    scene_parts=[build_pick_cube()],
    lighting=[Lighting(light_type="directional", position=(1.0, 1.0, 2.0))],
)
run_pick(sim, verbose=False)

capture(
    sim,
    sim.data.qpos.copy(),
    str(IMAGES_DIR / "arm_6dof.png"),
    lookat=[0.1, 0, 0.22],
    distance=0.8,
    azimuth=135,
    elevation=-18,
)
