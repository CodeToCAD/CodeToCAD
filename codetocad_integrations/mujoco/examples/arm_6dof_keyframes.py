"""Keyframe the 6-DOF arm and save an animated GIF (MuJoCo).

Rather than an interpolation loop, drive the arm like an animator: command
the joints to a pose, pin it with ``sim.set_keyframe(t)``, repeat, then let
``sim.record_gif(keyframes=True)`` play the whole timeline back into a GIF.
The keyframe ledger interpolates each joint between the poses you pinned.

    python arm_6dof_keyframes.py

Reuses the arm from ``arm_6dof.py`` next door. Needs the mujoco + build123d
extras, and an OpenGL context for offscreen rendering (any desktop; headless
CI without EGL/OSMesa can't render).
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from arm_6dof import FINGER_TRAVEL, arm_pose, build_arm

from codetocad import Lighting
from codetocad_integrations.mujoco import simulate

GIF_PATH = Path(__file__).resolve().parent / "images" / "arm_6dof_keyframes.gif"


def choreography() -> list[tuple[str, float, dict[str, float]]]:
    """(label, seconds to reach it, joint targets) poses to keyframe through.
    Targets are cumulative: joints you don't mention hold their last value."""
    return [
        ("reach out", 1.5, arm_pose(0.28, 0.12)),
        ("sweep left", 1.2, {"joint1": 1.2}),
        ("sweep right", 1.4, {"joint1": -1.2}),
        ("wrist flourish", 1.0, {"joint1": 0.0, "joint4": 1.0, "joint6": 1.2}),
        (
            "close gripper",
            0.7,
            {"left_finger": FINGER_TRAVEL, "right_finger": -FINGER_TRAVEL},
        ),
        (
            "open + home",
            1.6,
            {
                "left_finger": 0.0, "right_finger": 0.0,
                "joint2": 0.0, "joint3": 0.0,
                "joint4": 0.0, "joint5": 0.0, "joint6": 0.0,
            },
        ),
    ]


def set_keyframes(sim) -> None:
    # Start from the home pose so the first keyframe pins every joint at 0.
    for name in sim.joint_names:
        sim.get_joint(name).move_to(0.0)
    at = sim.set_keyframe(0.0)
    for label, duration, targets in choreography():
        for name, value in targets.items():
            sim.get_joint(name).move_to(value)
        at = sim.set_keyframe(at + duration)


def main() -> None:
    sim = simulate(
        build_arm(),
        lighting=[Lighting(light_type="directional", position=(1.0, 1.0, 2.0))],
        # Pose the arm smoothly in free space: turn self-collision off so the
        # straight arm's convex hulls don't jam on each other (we're posing,
        # not making contact). The position servo's velocity feedback keeps
        # the hold from oscillating.
        self_collision=False,
    )
    set_keyframes(sim)
    GIF_PATH.parent.mkdir(parents=True, exist_ok=True)
    sim.record_gif(GIF_PATH, keyframes=True, fps=20, width=480, height=480)
    sim.close()
    print(f"wrote {GIF_PATH}")


if __name__ == "__main__":
    main()
