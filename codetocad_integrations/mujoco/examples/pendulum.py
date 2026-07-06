"""A pendulum modeled with Build123D and simulated in MuJoCo: a rod hinged
to a fixed mount with a bob fixed to its end, released from 60 degrees and
left to swing freely (actuated=False -> no actuators, pure dynamics).

Run (macOS needs mjpython for the viewer):  mjpython pendulum.py
Headless test (any python):                 python pendulum.py --test
"""

import math
import sys

from codetocad import Location, aluminum_material, red_material
from codetocad_integrations.build123d import make_cube, make_cylinder, make_sphere
from codetocad_integrations.mujoco import simulate


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
    sim = simulate(build_pendulum(), actuated=False)
    sim.set_joint_value("pivot", math.radians(60))

    if test_mode:
        for second in range(6):
            angle = math.degrees(sim.get_joint_value("pivot"))
            print(f"t={second * 0.5:4.1f}s  angle={angle:+7.2f} deg")
            sim.run(0.5)
        return

    try:
        sim.launch_viewer()
    except RuntimeError as error:
        print(f"Could not open the MuJoCo viewer: {error}")
        print("On macOS, run this example with mjpython instead of python.")


if __name__ == "__main__":
    main()
