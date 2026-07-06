"""A 6-DOF robot arm modeled with Build123D and simulated in PyBullet.

Keyboard control (in the PyBullet GUI window):
    a / s / d / f / g / h   move joints 1-6
    hold Shift              reverse the direction of the joint value

Run:            python arm_6dof.py
Headless test:  python arm_6dof.py --test
"""

import math
import sys
import time

from codetocad import Lighting, Location, aluminum_material, red_material
from codetocad_integrations.build123d import make_cylinder
from codetocad_integrations.pybullet import simulate

KEYS = "asdfgh"


def z_joint(z: float, name: str) -> Location:
    """A revolute joint about the world Z axis."""
    return Location(z=z, name=name)


def y_joint(z: float, name: str) -> Location:
    """A revolute joint about the world Y axis (Z axis rotated by -90 deg
    about X)."""
    return Location.from_euler(0, 0, z, x_deg=-90, name=name)


def build_arm():
    base = make_cylinder("4cm", "6cm", start_location=Location(z="3cm"))
    base.name = "base"
    base.set_material(aluminum_material())
    # (name, radius, z_from, z_to, joint, limits)
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
        gui=not test_mode,
        lighting=[Lighting(light_type="point", position=(1.0, 1.0, 2.0))],
    )
    names = sim.joint_names

    if test_mode:
        goals = (0.5, 0.4, -0.6, 0.8, 0.5, -1.0)
        for name, goal in zip(names, goals):
            sim.set_joint_target(name, goal)
        sim.run(5.0)
        for name, goal in zip(names, goals):
            print(f"{name}: target {goal:+.2f} -> {sim.get_joint_value(name):+.3f}")
        sim.close()
        return

    import pybullet as p

    print(f"Joints: {names}")
    print("Keys a/s/d/f/g/h move joints 1-6; hold Shift to reverse.")
    targets = dict.fromkeys(names, 0.0)
    step_size = math.radians(1.0)
    while sim.is_connected():
        events = sim.get_keyboard_events()
        reverse = events.get(p.B3G_SHIFT, 0) & p.KEY_IS_DOWN
        direction = -1.0 if reverse else 1.0
        for index, key in enumerate(KEYS):
            if events.get(ord(key), 0) & p.KEY_IS_DOWN:
                name = names[index]
                targets[name] += direction * step_size
                sim.set_joint_target(name, targets[name])
        sim.step()
        time.sleep(sim.time_step)


if __name__ == "__main__":
    main()
