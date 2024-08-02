from codetocad import *

Scene.default().set_default_unit("cm")
Scene.default().create_group("Bracelet")


class Bracelet:
    outer_diameter = "161cm"
    inner_diameter = "81cm"
    thickness = "83cm"

    def create(self):
        bracelet = Part("bracelet").create_torus(
            Dimension.from_string(self.inner_diameter) / 2,
            Dimension.from_string(self.outer_diameter) / 2,
        )
        bracelet.scale_z(self.thickness)

        return bracelet


class Button:
    radius = "60/2cm"
    depth = "13.6cm"
    inset_radius = "20cm"
    inset_depth = "3cm"

    def create(self):
        button = Part("button").create_cylinder(self.radius, self.depth)
        button_top = button.get_landmark("top")
        button.hole(button_top, self.inset_radius, self.inset_depth)
        button.fillet_faces("5cm", [button_top])
        return button


class Belt:
    outer_radius = "163/2cm"
    inner_radius = "150/2cm"
    thickness = "30cm"

    def create(self):
        belt = Part("belt").create_cylinder(self.outer_radius, self.thickness)
        belt.hole(belt.get_landmark("top"), self.inner_radius, self.thickness)
        return belt


if __name__ == "__main__":
    # MARK: Create components
    bracelet = Bracelet().create()
    button = Button().create()
    belt = Belt().create()

    # Mark: Joint the button to the front of the bracelet
    Joint(
        bracelet.get_landmark("front"), button.get_landmark("top")
    ).limit_location_xyz(0, 0, 0).limit_rotation_xyz(90, 0, 0)
    Joint(
        bracelet.get_landmark("center"), belt.get_landmark("center")
    ).limit_location_xyz(0, 0, 0).limit_rotation_xyz(0, 0, 0)

    # # Mark: subtract the button and belt from the bracelet:
    bracelet.subtract(belt, delete_after_subtract=False)

    bracelet.hole(
        belt.get_landmark("front"),
        button.get_dimensions().x / 2,
        button.get_dimensions().z,
        normal_axis="y",
        flip_axis=True,
    )
    belt.hole(
        belt.get_landmark("front"),
        button.get_dimensions().x / 2,
        belt.get_dimensions().z,
        normal_axis="y",
        flip_axis=True,
    )

    # # Mark: Assign to a group:

    # Scene().assign_to_group([bracelet, button, belt], "Bracelet")

    # Mark apply materials:
    red_material = Material("red").set_color(181, 16, 4)
    blue_material = Material("blue").set_color(19, 107, 181)

    bracelet.set_material(red_material)
    button.set_material(blue_material)
    belt.set_material(blue_material)
