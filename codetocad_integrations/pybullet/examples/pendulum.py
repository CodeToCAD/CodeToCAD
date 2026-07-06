"""A pendulum modeled with Build123D and simulated in PyBullet: a rod
hinged to a fixed mount with a bob fixed to its end, released from 60
degrees and left to swing freely.

Run:            python pendulum.py
Headless test:  python pendulum.py --test
"""

import math
import sys
import time

from codetocad import Location, aluminum_material, red_material
from codetocad_integrations.build123d import make_cube, make_cylinder, make_sphere
from codetocad_integrations.pybullet import simulate


def build_pendulum():
    mount = make_cube("6cm", "6cm", "4cm", start_location=Location(z="52cm"))
    mount.name = "mount"
    mount.set_material(aluminum_material())
    rod = make_cylinder("1cm", "40cm", start_location=Location(z="30cm"))
    rod.name = "rod"
    bob = make_sphere("5cm", start_location=Location(z="10cm"))
    bob.name = "bob"
    bob.set_material(red_material())

    pivot = Location.from_euler(0, 0, "50cm", x_deg=-90, name="pivot")
    mount.revolute(pivot, rod, pivot)  # hinge about the Y axis
    rod.fixed(Location(z="10cm"), bob, Location(z="10cm"))
    return mount


def main() -> None:
    test_mode = "--test" in sys.argv
    sim = simulate(build_pendulum(), gui=not test_mode)
    sim.set_joint_value("pivot", math.radians(60))

    duration = 3.0 if test_mode else 30.0
    steps = int(duration / sim.time_step)
    for step in range(steps):
        sim.step()
        if not test_mode:
            time.sleep(sim.time_step)
        if step % 120 == 0:
            angle = math.degrees(sim.get_joint_value("pivot"))
            print(f"t={step * sim.time_step:5.2f}s  angle={angle:+7.2f} deg")
        if not test_mode and not sim.is_connected():
            break
    sim.close()


if __name__ == "__main__":
    main()
