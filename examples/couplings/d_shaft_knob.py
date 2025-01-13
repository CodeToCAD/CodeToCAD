from codetocad import *
from codetocad.interfaces.part_interface import PartInterface
from .d_shaft import DShaft


def create_d_shaft_sleeve(d_shaft: PartInterface, sleeve_thickness):
    d_shaft_diameter = d_shaft.get_dimensions().y

    sleeve = Part.create_cylinder(
        d_shaft_diameter / 2 + sleeve_thickness, d_shaft.get_dimensions().z
    )

    sleeve.subtract(d_shaft, is_transfer_data=True)

    return sleeve


def create_knob(radius):
    knob = Sketch.create_polygon(7, radius, radius).extrude(radius * 0.2)

    return knob


if __name__ == "__main__":
    Scene.default().set_default_unit("mm")

    shaft_length = Dimension.from_string("13.65mm")
    radius = Dimension.from_string("5.9/2mm")
    d_profile_radius = Dimension.from_string("5.3/2mm")
    d_profile_length = shaft_length
    tolerance = Dimension.from_string("0.15mm")

    d_shaft = DShaft(
        shaft_length=shaft_length,
        radius=radius,
        d_profile_radius=d_profile_radius,
        d_profile_length=d_profile_length,
        tolerance=tolerance,
    ).create("shaft")

    sleeve = create_d_shaft_sleeve(d_shaft, "1.5mm")

    knob = create_knob(sleeve.get_dimensions().x)

    Joint(
        sleeve.create_landmark("top", center, center, max),
        knob.create_landmark("bottom", center, center, min),
    ).limit_location_xyz(0, 0, 0)

    sleeve.union(knob)
    # sleeve.export("./appliance_knob.stl", scale=1000)
