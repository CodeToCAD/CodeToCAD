"""Generate images/arm_6dof.png: the 6-DOF arm holding the picked-up cube,
screenshot headlessly.

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

from arm_6dof import build_arm, build_pick_cube, run_pick
from codetocad import Lighting
from codetocad_integrations.pybullet import simulate
from _render_common import capture

sim = simulate(
    build_arm(),
    gui=False,
    ground_plane=True,
    scene_parts=[build_pick_cube()],
    lighting=[Lighting(light_type="point", position=(1.0, 1.0, 2.0))],
)
run_pick(sim, verbose=False)

capture(
    sim,
    str(IMAGES_DIR / "arm_6dof.png"),
    eye=[0.62, 0.62, 0.5],
    target=[0.1, 0, 0.22],
    fov=45,
)
sim.close()
