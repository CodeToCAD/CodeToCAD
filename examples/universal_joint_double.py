from codetocad import *
from universal_joint import Yoke, Cross


def createDoubleuniversal_joint():
    shaft_radius = Dimension.from_string("5mm")
    wall_thickness = Dimension.from_string("3mm")
    shaft_length = Dimension.from_string("15mm")
    center_yold_length = Dimension.from_string("5mm")
    pin_arm_length = Dimension.from_string("13mm")
    pin_hole_radius = Dimension.from_string("2mm")
    set_screw_radius = Dimension.from_string("3mm")

    yoke_center = Yoke(
        shaft_radius=shaft_radius,
        wall_thickness=wall_thickness,
        shaft_length=center_yold_length,
        pin_arm_length=pin_arm_length,
        pin_hole_radius=pin_hole_radius,
        set_screw_radius=set_screw_radius,
        is_hollowed=False,
    ).create("yokeCenter")
    yoke_center_pin_top = yoke_center.get_landmark("pinArm_pin")
    yoke_center_pin_top_location = yoke_center_pin_top.get_location_local()
    yoke_center_bottom_z = (
        yoke_center.get_landmark(PresetLandmark.bottom).get_location_local().z
    )
    yoke_center.mirror(yoke_center.get_landmark(PresetLandmark.bottom), "z", None)
    yoke_center_pin_bottom = yoke_center.create_landmark(
        "pinBottom",
        yoke_center_pin_top_location.x,
        yoke_center_pin_top_location.y,
        yoke_center_pin_top_location.z * -1 + yoke_center_bottom_z * 2,
    )

    yoke_top = Yoke(
        shaft_radius=shaft_radius,
        wall_thickness=wall_thickness,
        shaft_length=shaft_length,
        pin_arm_length=pin_arm_length,
        pin_hole_radius=pin_hole_radius,
        set_screw_radius=set_screw_radius,
    ).create("yokeTop")
    yoke_top.rotate_y(180)
    yoke_top.rotate_z(90)

    yokeBottom = Yoke(
        shaft_radius=shaft_radius,
        wall_thickness=wall_thickness,
        shaft_length=shaft_length,
        pin_arm_length=pin_arm_length,
        pin_hole_radius=pin_hole_radius,
        set_screw_radius=set_screw_radius,
    ).create("yokeBottom")
    yokeBottom.rotate_z(90)

    cross1 = Cross(
        width=shaft_radius,
        pin_radius=pin_hole_radius,
        pin_length=shaft_radius / 2 + wall_thickness,
    ).create("cross1")

    cross2 = Cross(
        width=shaft_radius,
        pin_radius=pin_hole_radius,
        pin_length=shaft_radius / 2 + wall_thickness,
    ).create("cross2")

    Joint(
        cross1.get_landmark(PresetLandmark.right),
        yoke_top.get_landmark("pinArm_pin"),
    ).limit_rotation_xyz(None, 0, 0).limit_rotation_x(-45, 45).limit_location_xyz(
        0, 0, 0
    )

    Joint(
        cross1.get_landmark(PresetLandmark.front), yoke_center_pin_top
    ).limit_rotation_xyz(0, None, 0).limit_rotation_y(-45, 45).limit_location_xyz(
        0, 0, 0
    )

    Joint(
        yoke_center_pin_bottom,
        cross2.get_landmark(PresetLandmark.front),
    ).limit_rotation_xyz(None, 0, 0).limit_rotation_x(-45, 45).limit_location_xyz(
        0, 0, 0
    )

    Joint(
        cross2.get_landmark(PresetLandmark.right), yokeBottom.get_landmark("pinArm_pin")
    ).limit_rotation_xyz(None, 0, 0).limit_rotation_x(-45, 45).limit_location_xyz(
        0, 0, 0
    )


if __name__ == "__main__":
    createDoubleuniversal_joint()
