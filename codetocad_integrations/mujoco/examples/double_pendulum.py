"""A chaotic double pendulum modeled with Build123D and simulated in MuJoCo:
two rod+bob links chained with revolute joints, released from horizontal
(actuated=False -> no actuators, pure dynamics).

Run (macOS needs mjpython for the viewer):  mjpython double_pendulum.py
Headless test (any python):                 python double_pendulum.py --test
"""

import math
import sys

from codetocad import Location, aluminum_material, green_material, red_material
from codetocad_integrations.build123d import make_cube, make_cylinder, make_sphere
from codetocad_integrations.mujoco import simulate


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
    sim = simulate(build_double_pendulum(), actuated=False)
    sim.set_joint_value("pivot1", math.radians(90))
    sim.set_joint_value("pivot2", 0.0)

    if test_mode:
        for second in range(5):
            angle1 = math.degrees(sim.get_joint_value("pivot1"))
            angle2 = math.degrees(sim.get_joint_value("pivot2"))
            print(
                f"t={second:4.1f}s  pivot1={angle1:+8.2f} deg  "
                f"pivot2={angle2:+8.2f} deg"
            )
            sim.run(1.0)
        return

    try:
        sim.launch_viewer()
    except RuntimeError as error:
        print(f"Could not open the MuJoCo viewer: {error}")
        print("On macOS, run this example with mjpython instead of python.")


if __name__ == "__main__":
    main()
