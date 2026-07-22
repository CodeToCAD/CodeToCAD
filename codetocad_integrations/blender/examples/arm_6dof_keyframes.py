"""Keyframe a 6-DOF arm and save an animated GIF (Blender).

The Blender simulation backend realizes each joint as an empty at the joint
anchor (its local Z is the joint axis), parents the parts into a live rig, and
holds commanded poses with Blender's **native keyframing**. So the animator
workflow is: command the joints to a pose, pin it with ``sim.set_keyframe(t)``
(which inserts real Blender keyframes on the joint empties), then
``sim.record_gif(keyframes=True)`` plays the timeline back into a GIF.

    python arm_6dof_keyframes.py

Run it like any Blender design: ``ensure_blender()`` relaunches this script
under ``blender --background`` if you started it with a normal Python. Set
``CODETOCAD_BLENDER`` to point at your Blender executable if it isn't on PATH.

``sim.launch_viewer()`` (commented at the bottom) instead opens a Blender GUI
on the rig and plays the keyframed animation.
"""

import math
from pathlib import Path

from codetocad import Location, aluminum_material, red_material, steel_material
from codetocad_integrations.blender import ensure_blender

GIF_PATH = Path(__file__).resolve().parent / "images" / "arm_6dof_keyframes.gif"

FINGER_TRAVEL = 0.026  # prismatic travel of each gripper finger


def z_joint(z: float, name: str) -> Location:
    """A revolute/prismatic axis pointing up (a location's axis is its Z)."""
    return Location(z=z, name=name)


def y_joint(z: float, name: str) -> Location:
    """A hinge axis pointing +Y (x_deg=-90 turns the location's Z onto Y)."""
    return Location.from_euler(0, 0, z, x_deg=-90, name=name)


def build_arm(make_cube, make_cylinder):
    """A blocky 6-DOF arm with a parallel-jaw gripper: alternating yaw
    (vertical) and pitch (horizontal) joints stacked up a column, then two
    fingers on prismatic joints. Parts are modeled in place; each joint is
    placed where two links meet."""
    base = make_cube("12cm", "12cm", "5cm", start_location=Location(z=0.025))
    base.name = "base"
    base.set_material(aluminum_material())

    # joint1 yaw at z=0.05
    link1 = make_cylinder("3cm", "8cm", start_location=Location(z=0.09))
    link1.name = "link1"
    link1.set_material(red_material())
    base.revolute(
        z_joint(0.05, "joint1"), link1, z_joint(0.05, "joint1"),
        min_limits=-math.pi, max_limits=math.pi,
    )

    # joint2 pitch at z=0.13
    link2 = make_cube("4cm", "4cm", "16cm", start_location=Location(z=0.21))
    link2.name = "link2"
    link2.set_material(aluminum_material())
    link1.revolute(
        y_joint(0.13, "joint2"), link2, y_joint(0.13, "joint2"),
        min_limits=-2.1, max_limits=2.1,
    )

    # joint3 pitch at z=0.29
    link3 = make_cube("4cm", "4cm", "13cm", start_location=Location(z=0.355))
    link3.name = "link3"
    link3.set_material(red_material())
    link2.revolute(
        y_joint(0.29, "joint3"), link3, y_joint(0.29, "joint3"),
        min_limits=-2.4, max_limits=2.4,
    )

    # joint4 yaw at z=0.42
    link4 = make_cylinder("2.5cm", "5cm", start_location=Location(z=0.445))
    link4.name = "link4"
    link4.set_material(aluminum_material())
    link3.revolute(
        z_joint(0.42, "joint4"), link4, z_joint(0.42, "joint4"),
        min_limits=-math.pi, max_limits=math.pi,
    )

    # joint5 pitch at z=0.47
    link5 = make_cube("4cm", "4cm", "8cm", start_location=Location(z=0.51))
    link5.name = "link5"
    link5.set_material(red_material())
    link4.revolute(
        y_joint(0.47, "joint5"), link5, y_joint(0.47, "joint5"),
        min_limits=-2.2, max_limits=2.2,
    )

    # joint6 yaw at z=0.55, plus the gripper palm as one rigid link
    link6 = make_cube("5cm", "5cm", "2cm", start_location=Location(z=0.56))
    link6.name = "link6"
    palm = make_cube("11cm", "4cm", "2cm", start_location=Location(z=0.58))
    link6.union(other_part=palm)
    link6.set_material(aluminum_material())
    link5.revolute(
        z_joint(0.55, "joint6"), link6, z_joint(0.55, "joint6"),
        min_limits=-math.pi, max_limits=math.pi,
    )

    # Parallel-jaw gripper: two fingers sliding along +X (the left finger
    # closes with a positive value, the right with a negative one).
    for side, x, lower, upper in (
        ("left_finger", -0.04, 0.0, FINGER_TRAVEL),
        ("right_finger", 0.04, -FINGER_TRAVEL, 0.0),
    ):
        finger = make_cube("1.4cm", "3.2cm", "6cm", start_location=Location(x=x, z=0.62))
        finger.name = side
        finger.set_material(steel_material())
        slide = Location.from_euler(x, 0, 0.59, y_deg=90, name=side)
        link6.prismatic(slide, finger, slide, min_limits=lower, max_limits=upper)

    return base


def choreography() -> list[tuple[str, float, dict[str, float]]]:
    """(label, seconds to reach it, joint targets) poses to keyframe through.
    Targets are cumulative: joints you don't mention hold their last value."""
    return [
        ("reach out", 1.5, {"joint2": 0.6, "joint3": -1.0, "joint5": 0.5}),
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
    from codetocad_integrations.blender import make_cube, make_cylinder, simulate

    sim = simulate(build_arm(make_cube, make_cylinder), fps=20)
    set_keyframes(sim)
    GIF_PATH.parent.mkdir(parents=True, exist_ok=True)
    sim.record_gif(GIF_PATH, keyframes=True, fps=20, width=480, height=480)
    print(f"wrote {GIF_PATH}")

    # Or, instead of a GIF, open a Blender GUI on the rig and play it back:
    # sim.launch_viewer()


if __name__ == "__main__":
    ensure_blender()  # relaunch under Blender if needed; reset the scene inside
    main()
