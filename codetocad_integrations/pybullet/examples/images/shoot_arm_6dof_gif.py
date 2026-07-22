"""Generate images/arm_6dof.gif: the 6-DOF arm picks the cube up off the
floor with its parallel-jaw gripper, headlessly.

    python shoot_arm_6dof_gif.py

Requires the pybullet + build123d extras (a venv with pybullet built, e.g.
this repo's .venv-sim, works well since pybullet needs a C build step).
"""
import sys
from pathlib import Path

EXAMPLES_DIR = Path(__file__).resolve().parent.parent
IMAGES_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(EXAMPLES_DIR))
sys.path.insert(0, str(IMAGES_DIR))

from arm_6dof import GRIP_FORCE, build_arm, build_pick_cube, pick_sequence

from codetocad import Lighting
from codetocad_integrations.pybullet import simulate

from _render_common import record_gif

SETTLE = 0.3  # pause between pick phases, as in the example's run_pick

sim = simulate(
    build_arm(),
    gui=False,
    ground_plane=True,
    scene_parts=[build_pick_cube()],
    lighting=[Lighting(light_type="point", position=(1.0, 1.0, 2.0))],
)
targets = dict.fromkeys(sim.joint_names, 0.0)
for name in targets:
    sim.get_joint(name).move_to(0.0)

# Unroll the pick sequence into (begin, end, start values, goals) phases
# so joint targets can be interpolated from the recording clock.
phases, clock, state = [], 0.0, dict(targets)
for label, duration, goals in pick_sequence():
    starts = {name: state[name] for name in goals}
    phases.append((clock, clock + duration, starts, goals))
    state.update(goals)
    clock += duration + SETTLE


def drive(t: float) -> None:
    for begin, end, starts, goals in phases:
        if t < begin:
            break
        fraction = min(1.0, (t - begin) / (end - begin))
        for name, goal in goals.items():
            value = starts[name] + (goal - starts[name]) * fraction
            force = GRIP_FORCE if "finger" in name else 100.0
            sim.get_joint(name).move_to(value, force=force)


record_gif(
    sim,
    str(IMAGES_DIR / "arm_6dof.gif"),
    duration_seconds=clock + 0.5,
    fps=15,
    on_frame=drive,
    eye=[0.62, 0.62, 0.5],
    target=[0.14, 0, 0.2],
    fov=45,
)
sim.close()
