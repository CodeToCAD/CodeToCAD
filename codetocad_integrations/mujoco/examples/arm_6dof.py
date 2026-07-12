"""A 6-DOF robot arm with a parallel-jaw gripper, modeled with Build123D
and simulated in MuJoCo.

Every joint is modeled as visible hardware, not an abstract frame:

- Pitch (hinge) joints: the parent link ends in a clevis — a slot cut
  out of its cube with a pin hole drilled through both prongs — and the
  child link's tongue swings inside it on a cylinder pin that sticks
  out of the clevis. The pin is the joint axis.
- Yaw joints: the child link stands on a cylinder neck seated in a
  round recess cut into the parent's top face; the neck is visible in
  the gap between the two cubes and is the joint axis.
- The gripper is two cube fingers on prismatic joints that slide along
  the palm.

A 3 cm cube sits on the floor in front of the arm to pick up.

Keyboard control (in the MuJoCo viewer window):
    a / s / d / f / g / h   move joints 1-6
    j / k                   close / open the gripper
    Shift (tap)             toggles/reverses the direction of joint motion

Run (macOS needs mjpython for the viewer):  mjpython arm_6dof.py
Headless test (any python):                 python arm_6dof.py --test
runs a scripted pick-and-lift and reports whether the cube left the
floor.
"""

import math
import sys

from codetocad import (
    Lighting,
    Location,
    aluminum_material,
    green_material,
    red_material,
    steel_material,
)
from codetocad_integrations.build123d import make_cube, make_cylinder
from codetocad_integrations.mujoco import simulate

# GLFW keycodes: a s d f g h -> joints 1-6; j / k close/open the gripper;
# left/right shift reverses.
KEYCODE_TO_JOINT = {65: 0, 83: 1, 68: 2, 70: 3, 71: 4, 72: 5}
KEYCODE_CLOSE, KEYCODE_OPEN = 74, 75
SHIFT_KEYCODES = (340, 344)

BAR = 0.04  # square cross-section of the link cubes
TONGUE = 0.02  # thickness of the tab that rides inside a clevis slot
SLOT = 0.024  # clevis slot width: the tongue plus clearance
PIN_RADIUS = 0.01
FINGER_TRAVEL = 0.026  # prismatic travel of each gripper finger
GRIP_CLOSED = 0.026  # travel that squeezes the cube (contact at 0.019)
CUBE_SIZE = 0.03
CUBE_X = 0.25  # where the pick cube sits on the floor

# Lever arms used by the scripted pick (planar 2-link IK).
SHOULDER_Z = 0.12  # joint2 height
L_UPPER = 0.16  # joint2 -> joint3
L_FORE = 0.13  # joint3 -> joint5
L_HAND = 0.16  # joint5 -> the grasp point between the fingertips


def z_joint(z: float, name: str) -> Location:
    """A revolute/prismatic axis pointing up (a location's joint axis is
    its rotated Z axis)."""
    return Location(z=z, name=name)


def y_joint(z: float, name: str) -> Location:
    """A hinge axis pointing +Y; positive angles tilt the arm towards +X."""
    return Location.from_euler(0, 0, z, x_deg=-90, name=name)


def hinge_pin(z: float, length: float):
    """The visible hinge hardware: a pin cylinder along Y (the hinge
    axis), long enough to stick out of both sides of the clevis."""
    pin = make_cylinder(PIN_RADIUS, length)
    pin.transform(relative=Location.from_euler(0, 0, z, x_deg=90))
    return pin


def cut_clevis(parent, joint_z: float, width: float) -> None:
    """Cut a clevis into the top of ``parent``: a slot for the child's
    tongue to swing in, plus a pin hole drilled through both prongs."""
    slot = make_cube(
        width + 0.01, SLOT, 0.06, start_location=Location(z=joint_z + 0.01)
    )
    parent.subtract(other_part=slot)
    parent.hole(
        Location(0, -width, joint_z),
        PIN_RADIUS + 0.002,
        end_location=Location(0, width, joint_z),
    )


def cut_recess(parent, top_z: float, neck_radius: float) -> None:
    """Cut the round socket into ``parent``'s top face that a yaw link's
    neck seats into."""
    parent.hole(Location(z=top_z), neck_radius + 0.002, amount=0.02)


def hinge_link(name: str, joint_z: float, parent_width: float, bar_top: float, material):
    """A link that pivots inside a parent's clevis: a square bar whose
    bottom tongue rides in the slot, unioned with the protruding pin."""
    bar = make_cube(
        BAR,
        BAR,
        bar_top - joint_z - 0.025,
        start_location=Location(z=(joint_z + 0.025 + bar_top) / 2),
    )
    bar.name = name
    tongue = make_cube(BAR, TONGUE, 0.05, start_location=Location(z=joint_z))
    bar.union(other_part=tongue)
    bar.union(other_part=hinge_pin(joint_z, parent_width + 0.02))
    bar.set_material(material)
    return bar


def yaw_link(
    name: str, joint_z: float, neck_radius: float, body_size: float, body_top: float, material
):
    """A link that swivels about vertical: a cube standing on a neck
    cylinder that seats into the parent's recess. The neck stays visible
    in the 1 cm gap between the two cubes."""
    body = make_cube(
        body_size,
        body_size,
        body_top - joint_z - 0.01,
        start_location=Location(z=(joint_z + 0.01 + body_top) / 2),
    )
    body.name = name
    neck = make_cylinder(neck_radius, 0.04, start_location=Location(z=joint_z + 0.002))
    body.union(other_part=neck)
    body.set_material(material)
    return body


def build_arm():
    base = make_cube(0.12, 0.12, 0.05, start_location=Location(z=0.025))
    base.name = "base"
    base.set_material(aluminum_material())
    cut_recess(base, 0.05, 0.02)

    # Shoulder yaw: a wide neck standing in the base's recess.
    link1 = yaw_link("link1", 0.05, 0.02, 0.06, 0.14, red_material())
    cut_clevis(link1, 0.12, 0.06)
    base.revolute(
        z_joint(0.05, "joint1"), link1, z_joint(0.05, "joint1"),
        min_limits=-math.pi, max_limits=math.pi,
    )

    # Shoulder pitch: the upper arm's tongue in link1's clevis.
    link2 = hinge_link("link2", 0.12, 0.06, 0.30, aluminum_material())
    cut_clevis(link2, 0.28, BAR)
    link1.revolute(
        y_joint(0.12, "joint2"), link2, y_joint(0.12, "joint2"),
        min_limits=-2.1, max_limits=2.1,
    )

    # Elbow pitch.
    link3 = hinge_link("link3", 0.28, BAR, 0.35, red_material())
    cut_recess(link3, 0.35, 0.012)
    link2.revolute(
        y_joint(0.28, "joint3"), link3, y_joint(0.28, "joint3"),
        min_limits=-2.4, max_limits=2.4,
    )

    # Wrist yaw.
    link4 = yaw_link("link4", 0.35, 0.012, 0.05, 0.43, aluminum_material())
    cut_clevis(link4, 0.41, 0.05)
    link3.revolute(
        z_joint(0.35, "joint4"), link4, z_joint(0.35, "joint4"),
        min_limits=-math.pi, max_limits=math.pi,
    )

    # Wrist pitch.
    link5 = hinge_link("link5", 0.41, 0.05, 0.48, red_material())
    cut_recess(link5, 0.48, 0.012)
    link4.revolute(
        y_joint(0.41, "joint5"), link5, y_joint(0.41, "joint5"),
        min_limits=-2.2, max_limits=2.2,
    )

    # Flange yaw + the gripper palm, one rigid link.
    link6 = make_cube(0.05, 0.05, 0.02, start_location=Location(z=0.50))
    link6.name = "link6"
    palm = make_cube(0.11, BAR, 0.02, start_location=Location(z=0.52))
    link6.union(other_part=palm)
    neck = make_cylinder(0.012, 0.04, start_location=Location(z=0.482))
    link6.union(other_part=neck)
    link6.set_material(aluminum_material())
    link5.revolute(
        z_joint(0.48, "joint6"), link6, z_joint(0.48, "joint6"),
        min_limits=-math.pi, max_limits=math.pi,
    )

    # Parallel-jaw gripper: two cube fingers sliding along the palm.
    # Both prismatic axes point +X, so the left finger closes with a
    # positive value and the right finger with a negative one.
    for side, x, lower, upper in (
        ("left_finger", -0.041, 0.0, FINGER_TRAVEL),
        ("right_finger", 0.041, -FINGER_TRAVEL, 0.0),
    ):
        finger = make_cube(0.014, 0.032, 0.06, start_location=Location(x=x, z=0.56))
        finger.name = side
        finger.set_material(steel_material())
        slide = Location.from_euler(x, 0, 0.53, y_deg=90, name=side)
        link6.prismatic(slide, finger, slide, min_limits=lower, max_limits=upper)

    return base


def build_pick_cube():
    cube = make_cube(
        CUBE_SIZE, CUBE_SIZE, CUBE_SIZE,
        start_location=Location(x=CUBE_X, z=CUBE_SIZE / 2),
    )
    cube.name = "pick_cube"
    cube.set_material(green_material())
    return cube


def arm_pose(reach_x: float, grasp_z: float) -> dict[str, float]:
    """Joint angles that put the grasp point at ``(reach_x, 0, grasp_z)``
    with the gripper pointing straight down: planar 2-link IK for the
    shoulder and elbow, then the wrist pitch makes the hand vertical."""
    dx, dz = reach_x, grasp_z + L_HAND - SHOULDER_Z
    reach_sq = dx * dx + dz * dz
    cos_elbow = (reach_sq - L_UPPER**2 - L_FORE**2) / (2 * L_UPPER * L_FORE)
    elbow = math.acos(max(-1.0, min(1.0, cos_elbow)))
    shoulder = math.atan2(dx, dz) - math.atan2(
        L_FORE * math.sin(elbow), L_UPPER + L_FORE * math.cos(elbow)
    )
    wrist = math.pi - shoulder - elbow
    return {"joint2": shoulder, "joint3": elbow, "joint5": wrist}


def pick_sequence() -> list[tuple[str, float, dict[str, float]]]:
    """(label, duration, joint targets) steps that pick up the cube."""
    grip = {"left_finger": GRIP_CLOSED, "right_finger": -GRIP_CLOSED}
    return [
        ("reach above the cube", 2.5, arm_pose(CUBE_X, 0.10)),
        # Grasp with the fingertips just above the floor: the grasp point
        # sits at the cube's top so the 6 cm fingers wrap its full height.
        ("descend around it", 1.5, arm_pose(CUBE_X, CUBE_SIZE)),
        ("close the gripper", 1.0, grip),
        ("lift", 2.0, arm_pose(0.18, 0.16)),
    ]


def run_pick(sim, verbose: bool = True) -> float:
    """Run the scripted pick-and-lift, ramping the joint targets so the
    servos track instead of overshooting; returns the cube's final height."""
    targets = dict.fromkeys(sim.joint_names, 0.0)
    for name, value in targets.items():
        sim.set_joint_target(name, value)  # hold every joint, fingers included
    for label, duration, goals in pick_sequence():
        if verbose:
            print(label)
        start = dict(targets)
        steps = max(1, round(duration / 0.02))
        for step in range(1, steps + 1):
            fraction = step / steps
            for name, goal in goals.items():
                targets[name] = start[name] + (goal - start[name]) * fraction
                sim.set_joint_target(name, targets[name])
            sim.run(duration / steps)
        sim.run(0.3)  # settle
    return sim.get_body_pose("pick_cube")[0][2]


def main() -> None:
    test_mode = "--test" in sys.argv
    sim = simulate(
        build_arm(),
        ground_plane=True,
        scene_parts=[build_pick_cube()],
        lighting=[Lighting(light_type="directional", position=(1.0, 1.0, 2.0))],
    )
    names = sim.joint_names

    if test_mode:
        height = run_pick(sim)
        picked = height > CUBE_SIZE * 2
        print(
            f"cube height after lift: {height:.3f} m "
            f"({'picked up' if picked else 'still on the floor'})"
        )
        return

    print(f"Joints: {names}")
    print(
        "Keys a/s/d/f/g/h move joints 1-6, j/k close/open the gripper; "
        "tap Shift to reverse direction."
    )
    targets = dict.fromkeys(names, 0.0)
    state = {"direction": 1.0}
    step_size = math.radians(3.0)
    grip_step = 0.0015

    def move_gripper(delta: float) -> None:
        travel = min(
            FINGER_TRAVEL, max(0.0, targets["left_finger"] + delta)
        )
        targets["left_finger"] = travel
        targets["right_finger"] = -travel
        sim.set_joint_target("left_finger", travel)
        sim.set_joint_target("right_finger", -travel)

    def on_key(keycode: int) -> None:
        if keycode in SHIFT_KEYCODES:
            state["direction"] *= -1.0
            sign = "+" if state["direction"] > 0 else "-"
            print(f"direction: {sign}")
            return
        if keycode == KEYCODE_CLOSE:
            move_gripper(grip_step)
            return
        if keycode == KEYCODE_OPEN:
            move_gripper(-grip_step)
            return
        index = KEYCODE_TO_JOINT.get(keycode)
        if index is None:
            return
        name = names[index]
        targets[name] += state["direction"] * step_size
        sim.set_joint_target(name, targets[name])

    try:
        sim.launch_viewer(key_callback=on_key)
    except RuntimeError as error:
        print(f"Could not open the MuJoCo viewer: {error}")
        print("On macOS, run this example with mjpython instead of python.")


if __name__ == "__main__":
    main()
