from dataclasses import dataclass
from codetocad import *

blue_metallic_material = (
    Material("blue").set_color(0.0865257, 0.102776, 0.709804, 0.8).set_reflectivity(1.0)
)
red_metallic_material = (
    Material("red").set_color(0.709804, 0.109394, 0.245126, 0.8).set_reflectivity(1.0)
)


@dataclass
class Yoke:
    """
     A class that creates the arm of a universal joint:
     ___  ____________  __
    ( )                   )  < hollow rod
     ⁻⁻⁻  ⁻⁻⁻⁻⁻⁻⁻⁻⁻⁻⁻⁻  ⁻⁻
         ^             ^
      setScrew       pinHole
    """

    shaft_radius: Dimension
    wall_thickness: Dimension
    shaft_length: Dimension

    pin_arm_length: Dimension
    pin_hole_radius: Dimension
    set_screw_radius: Dimension

    is_hollowed: bool = True

    def _createHollowRod(self, name: str, length: Dimension) -> Part:
        outerRadius = self.shaft_radius + self.wall_thickness

        rod = Part.create_cylinder(outerRadius, length)

        if self.is_hollowed:
            rod.hollow(
                self.wall_thickness,
                self.wall_thickness,
                self.wall_thickness / 2,
                flip_axis=True,
            )

        _ = rod.create_landmark(
            "wallFront", center, f"min + {self.wall_thickness/4}", max
        )

        return rod

    def _create_shaft_coupling(self) -> Part:
        shaft_coupling = self._createHollowRod("shaftCoupling", self.shaft_length)

        if self.is_hollowed:
            shaft_coupling.hole(
                shaft_coupling.get_landmark(PresetLandmark.back),
                self.set_screw_radius,
                shaft_coupling.get_dimensions().y,
                normal_axis="y",
            )

        return shaft_coupling

    def _create_pin_arm(self) -> Part:
        pin_arm = self._createHollowRod("pinArm", self.pin_arm_length)

        pin_arm_size = pin_arm.get_dimensions()

        pin_arm_discard_Amount = 1 / 15

        pin_arm.subtract(
            Part("pinArmDiscard")
            .create_cube(
                pin_arm_size.x,
                pin_arm_size.y * (1 - pin_arm_discard_Amount),
                pin_arm_size.z + "1mm",
            )
            .translate_y(pin_arm_size.y * pin_arm_discard_Amount)
        )

        pin_arm.rotate_y(180)

        pin_location = pin_arm.create_landmark(
            "pin", center, min, "max -  (max-min) * 1/4"
        )

        pin_arm.hole(
            pin_location,
            self.pin_hole_radius,
            pin_arm_size.y,
            normal_axis="y",
            flip_axis=True,
        )

        # pinArm.fillet_faces(
        #     "25mm",
        #     [pinArm.get_landmark(PresetLandmark.top)]
        # )

        return pin_arm

    def create(self, name: str) -> Part:
        shaft_coupling = self._create_shaft_coupling()

        pin_arm = self._create_pin_arm()

        Joint(
            shaft_coupling.get_landmark("wallFront"), pin_arm.get_landmark("wallFront")
        ).limit_location_xyz(0, 0, 0)

        pin_arm.mirror(shaft_coupling, "y", None)

        shaft_coupling.get_landmark(PresetLandmark.top)

        yoke = shaft_coupling.union(pin_arm, is_transfer_data=True)

        # shaftCoupling.fillet_faces(
        #     "25mm", [shaftCoupling.get_landmark(PresetLandmark.top)])

        yoke.set_name(name)

        yoke.set_material(blue_metallic_material)

        return yoke


@dataclass
class Cross:
    width: Dimension
    pin_radius: Dimension
    pin_length: Dimension

    def create(self, name: str) -> Part:
        core = Part.create_cube(self.width, self.width, self.width)

        pin = Part.create_cylinder(self.pin_radius, self.pin_length)

        Joint(
            core.get_landmark(PresetLandmark.top),
            pin.get_landmark(PresetLandmark.bottom),
        ).limit_location_xyz(0, 0, 0)

        pin.circular_pattern(
            4, 90, center_entity_or_landmark=core, normal_direction_axis="y"
        )

        core = core.union(pin)

        core.rotate_x(90)

        core.set_material(red_metallic_material)

        return core


def create_universal_joint():
    shaft_radius = Dimension.from_string("5mm")
    wall_thickness = Dimension.from_string("3mm")
    shaft_length = Dimension.from_string("15mm")
    pin_arm_length = Dimension.from_string("13mm")
    pin_hole_radius = Dimension.from_string("2mm")
    set_screw_radius = Dimension.from_string("3mm")

    yokeBottom = Yoke(
        shaft_radius=shaft_radius,
        wall_thickness=wall_thickness,
        shaft_length=shaft_length,
        pin_arm_length=pin_arm_length,
        pin_hole_radius=pin_hole_radius,
        set_screw_radius=set_screw_radius,
    ).create("yokeBottom")

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

    cross = Cross(
        width=shaft_radius,
        pin_radius=pin_hole_radius,
        pin_length=shaft_radius / 2 + wall_thickness,
    ).create("cross")

    Joint(
        cross.get_landmark(PresetLandmark.front), yokeBottom.get_landmark("pinArm_pin")
    ).limit_location_xyz(0, 0, 0).limit_rotation_xyz(0, None, 0).limit_rotation_y(
        -45, 45
    )

    Joint(
        cross.get_landmark(PresetLandmark.right), yoke_top.get_landmark("pinArm_pin")
    ).limit_location_xyz(0, 0, 0).limit_rotation_xyz(None, 0, 0).limit_rotation_x(
        -45, 45
    )


if __name__ == "__main__":
    create_universal_joint()
