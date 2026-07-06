"""A chaotic double pendulum modeled with Build123D and simulated in
PyBullet: two rod+bob links chained with revolute joints, released from
horizontal.

Run:            python double_pendulum.py
Headless test:  python double_pendulum.py --test
"""

import math
import sys
import time

from codetocad import Location, aluminum_material, green_material, red_material
from codetocad_integrations.build123d import make_cube, make_cylinder, make_sphere
from codetocad_integrations.pybullet import simulate


def build_double_pendulum():
    mount = make_cube("6cm", "6cm", "4cm", start_location=Location(z="64cm"))
    mount.name = "mount"
    mount.set_material(aluminum_material())

    rod1 = make_cylinder("1cm", "30cm", start_location=Location(z="47cm"))
    rod1.name = "rod1"
    bob1 = make_sphere("3cm", start_location=Location(z="32cm"))
    bob1.name = "bob1"
    bob1.set_material(red_material())

    rod2 = make_cylinder("8mm", "25cm", start_location=Location(z="19.5cm"))
    rod2.name = "rod2"
    bob2 = make_sphere("3cm", start_location=Location(z="7cm"))
    bob2.name = "bob2"
    bob2.set_material(green_material())

    pivot1 = Location.from_euler(0, 0, "62cm", x_deg=-90, name="pivot1")
    pivot2 = Location.from_euler(0, 0, "32cm", x_deg=-90, name="pivot2")
    mount.revolute(pivot1, rod1, pivot1)
    rod1.fixed(Location(z="32cm"), bob1, Location(z="32cm"))
    rod1.revolute(pivot2, rod2, pivot2)
    rod2.fixed(Location(z="7cm"), bob2, Location(z="7cm"))
    return mount


def main() -> None:
    test_mode = "--test" in sys.argv
    sim = simulate(build_double_pendulum(), gui=not test_mode)
    sim.set_joint_value("pivot1", math.radians(90))
    sim.set_joint_value("pivot2", 0.0)

    duration = 4.0 if test_mode else 60.0
    steps = int(duration / sim.time_step)
    for step in range(steps):
        sim.step()
        if not test_mode:
            time.sleep(sim.time_step)
        if step % 240 == 0:
            angle1 = math.degrees(sim.get_joint_value("pivot1"))
            angle2 = math.degrees(sim.get_joint_value("pivot2"))
            print(
                f"t={step * sim.time_step:5.2f}s  "
                f"pivot1={angle1:+8.2f} deg  pivot2={angle2:+8.2f} deg"
            )
        if not test_mode and not sim.is_connected():
            break
    sim.close()


if __name__ == "__main__":
    main()
