"""Exercises the Blender simulation backend end-to-end. Run inside Blender
(test_blender.py::test_blender_simulation does this automatically)."""

import math

from codetocad import Location
from codetocad_integrations.blender import ensure_blender

ensure_blender()

from codetocad_integrations.blender import (  # noqa: E402
    make_cube,
    make_cylinder,
    simulate,
)


def approx(actual, expected, tol=1e-3):
    assert math.isclose(actual, expected, abs_tol=tol), f"{actual} != {expected}"


base = make_cube("20cm", "20cm", "10cm")
base.name = "base"
arm = make_cylinder("2cm", "40cm", start_location=Location(z="40cm"))
arm.name = "arm"
# Hinge axis is Y (x_deg=-90 rotates the location's Z onto Y), so the
# Z-aligned arm swings in the XZ plane instead of spinning about itself.
pivot = Location.from_euler(0, 0, "10cm", x_deg=-90, name="shoulder")
hinge = base.revolute(
    pivot, arm, pivot,
    min_limits=-1.5, max_limits=1.5, starting_angle="30deg",
)
tip = make_cube("4cm", "4cm", "4cm", start_location=Location(z="70cm"))
tip.name = "tip"
arm.fixed(Location(z="60cm"), tip, Location(z="60cm"))

sim = simulate(base)
assert sim.joint_names == ["shoulder"], sim.joint_names
assert hinge.is_bound
approx(sim.get_joint_value("shoulder"), math.radians(30))  # starting_angle

import bpy  # noqa: E402

# The fixed tip rides along with the arm's rotation about the shoulder: its
# world position should move a lot as the hinge swings.
tip_obj = sim._control_object(sim.links[2])
hinge.move_to("0deg")
bpy.context.view_layer.update()
tip_rest = tip_obj.matrix_world.translation.copy()

hinge.move_to("90deg")
approx(hinge.get_angle().to_degrees(), 90.0)
bpy.context.view_layer.update()
tip_swung = tip_obj.matrix_world.translation.copy()
assert (tip_swung - tip_rest).length > 0.3, (tip_rest[:], tip_swung[:])

# Native keyframing records three keys on the joint empty.
sim.clear_keyframes()
hinge.move_to("0deg"); sim.set_keyframe(0.0)
hinge.move_to("90deg"); sim.set_keyframe(1.0)
hinge.move_to("-45deg"); sim.set_keyframe(2.0)
action = sim._joint_empty["shoulder"].animation_data.action
assert len(action.fcurves[0].keyframe_points) == 3

# capture_image renders the current pose.
image = sim.capture_image(width=160, height=120)
assert image.shape == (120, 160, 3), image.shape
assert image.dtype.name == "uint8"

# record_gif plays the keyframe timeline into an animated GIF.
gif = sim.record_gif(keyframes=True, fps=8, width=120, height=90)
assert gif[:6] == b"GIF89a"

# Velocity control advances the joint on each step.
sim.set_joint_value("shoulder", 0.0)
hinge.set_velocity("1rad/s")
sim.step(sim.fps)  # ~1 second
approx(sim.get_joint_value("shoulder"), 1.0, tol=0.05)

# launch_viewer saves a .blend (we don't open a GUI headless).
blend_path = sim.save()
assert blend_path.exists()

print("BLENDER_SIM_SMOKE_OK")
