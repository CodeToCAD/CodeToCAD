from dataclasses import dataclass, field
from codetocad import *
from codetocad.interfaces.part_interface import PartInterface


@dataclass
class DShaft:
    shaft_length: Dimension
    radius: Dimension
    d_profile_radius: Dimension
    d_profile_length: Dimension
    tolerance: Dimension = field(default_factory=lambda: Dimension(0))

    def create(self, name, is_d_shaft_both_sides=False) -> PartInterface:
        shaft_length = self.shaft_length
        radius = self.radius - self.tolerance
        dProfileRadius = self.d_profile_radius - self.tolerance

        d_profile_width = (radius - dProfileRadius) * 2

        shaft = Part.create_cylinder(radius, shaft_length)

        d_profile = Part.create_cube(d_profile_width, radius * 2, self.d_profile_length)

        shaft_left_side = shaft.get_landmark(PresetLandmark.leftTop)
        d_profile_left_side = d_profile.get_landmark(PresetLandmark.leftTop)

        Joint(shaft_left_side, d_profile_left_side).limit_location_xyz(0, 0, 0)

        if is_d_shaft_both_sides:
            d_profile.mirror(shaft, "z", None)

        shaft.subtract(d_profile)

        shaft.get_landmark(PresetLandmark.front).delete()

        return shaft


if __name__ == "__main__":
    shaft_length = Dimension.from_string("13.65mm")
    radius = Dimension.from_string("5.9/2mm")
    d_profile_radius = Dimension.from_string("5.3/2mm")
    d_profile_length = shaft_length / 2
    tolerance = Dimension.from_string("0.15mm")

    dShaft = DShaft(
        shaft_length=shaft_length,
        radius=radius,
        d_profile_radius=d_profile_radius,
        d_profile_length=d_profile_length,
        tolerance=tolerance,
    ).create("shaft")
