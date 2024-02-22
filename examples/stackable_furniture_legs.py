from codetocad import *

Scene().set_default_unit("mm")

ellipse_leg = Sketch("ellipse_leg").create_ellipse("14mm", "27mm").extrude("5/2in")
ellipse_leg_top = ellipse_leg.create_landmark("top", center, center, max)
ellipse_leg_bottom = ellipse_leg.create_landmark("bottom", center, center, min)

ellipse_leg_outer_cutout = (
    Sketch("ellipse_legOuterCutout").create_ellipse("14mm", "27mm").extrude("1in")
)
ellipse_leg_outer_cutout.hollow("3mm", "3mm", 0)
ellipse_leg_outer_cutout_top = ellipse_leg_outer_cutout.create_landmark(
    "top", center, center, max
)
ellipse_leg_outer_cutout.create_landmark("bottom", center, center, min)

Joint(ellipse_leg_top, ellipse_leg_outer_cutout_top).translate_landmark_onto_another()

ellipse_leg.hollow("5mm", "5mm", 0)
ellipse_leg.subtract(ellipse_leg_outer_cutout, is_transfer_data=True)

ellipse_leg2 = ellipse_leg.clone("Leg2")
Joint(
    ellipse_leg.get_landmark("ellipse_legOuterCutout_bottom"),
    ellipse_leg2.get_landmark("bottom"),
).limit_location_xyz(0, 0, 0).limit_location_z(0, 10).limit_rotation_xyz(0, 0, 0)


red_material = Material("red").set_color(0.709804, 0.109394, 0.245126, 0.9)
blue_material = Material("blue").set_color(0.0865257, 0.102776, 0.709804, 0.9)
ellipse_leg.set_material(red_material)
ellipse_leg2.set_material(blue_material)
