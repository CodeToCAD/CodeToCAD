"""A 6-DOF robot arm modeled with Build123D and simulated in MuJoCo.

Keyboard control (in the MuJoCo viewer window):
    a / s / d / f / g / h   move joints 1-6
    Shift (tap)             toggles/reverses the direction of joint motion

Run (macOS needs mjpython for the viewer):  mjpython arm_6dof.py
Headless test (any python):                 python arm_6dof.py --test
"""

import math
import sys

from codetocad import Lighting, Location, aluminum_material, red_material
from codetocad_integrations.build123d import make_cylinder
from codetocad_integrations.mujoco import simulate

# GLFW keycodes: a s d f g h -> joints 1-6; left/right shift reverses.
KEYCODE_TO_JOINT = {65: 0, 83: 1, 68: 2, 70: 3, 71: 4, 72: 5}
SHIFT_KEYCODES = (340, 344)


def z_joint(z: float, name: str) -> Location:
    return Location(z=z, name=name)


def y_joint(z: float, name: str) -> Location:
    return Location.from_euler(0, 0, z, x_deg=-90, name=name)


def build_arm():
    base = make_cylinder("4cm", "6cm", start_location=Location(z="3cm"))
    base.name = "base"
    base.set_material(aluminum_material())
    segments = [
        ("link1", "3cm", 0.06, 0.12, z_joint(0.06, "joint1"), (-math.pi, math.pi)),
        ("link2", "2.5cm", 0.12, 0.30, y_joint(0.12, "joint2"), (-2.1, 2.1)),
        ("link3", "2cm", 0.30, 0.46, y_joint(0.30, "joint3"), (-2.4, 2.4)),
        ("link4", "1.8cm", 0.46, 0.52, z_joint(0.46, "joint4"), (-math.pi, math.pi)),
        ("link5", "1.5cm", 0.52, 0.60, y_joint(0.52, "joint5"), (-2.0, 2.0)),
        ("link6", "1.2cm", 0.60, 0.64, z_joint(0.60, "joint6"), (-math.pi, math.pi)),
    ]
    parent = base
    for index, (name, radius, z0, z1, joint, (lower, upper)) in enumerate(segments):
        link = make_cylinder(radius, z1 - z0, start_location=Location(z=(z0 + z1) / 2))
        link.name = name
        link.set_material(red_material() if index % 2 else aluminum_material())
        parent.revolute(joint, link, joint, min_limits=lower, max_limits=upper)
        parent = link
    return base


def main() -> None:
    test_mode = "--test" in sys.argv
    arm = build_arm()
    sim = simulate(
        arm,
        lighting=[Lighting(light_type="directional", position=(1.0, 1.0, 2.0))],
    )
    names = sim.joint_names

    if test_mode:
        goals = (0.5, 0.4, -0.6, 0.8, 0.5, -1.0)
        for name, goal in zip(names, goals):
            sim.set_joint_target(name, goal)
        sim.run(5.0)
        for name, goal in zip(names, goals):
            print(f"{name}: target {goal:+.2f} -> {sim.get_joint_value(name):+.3f}")
        return

    print(f"Joints: {names}")
    print("Keys a/s/d/f/g/h move joints 1-6; tap Shift to reverse direction.")
    targets = dict.fromkeys(names, 0.0)
    state = {"direction": 1.0}
    step_size = math.radians(3.0)

    def on_key(keycode: int) -> None:
        if keycode in SHIFT_KEYCODES:
            state["direction"] *= -1.0
            sign = "+" if state["direction"] > 0 else "-"
            print(f"direction: {sign}")
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
