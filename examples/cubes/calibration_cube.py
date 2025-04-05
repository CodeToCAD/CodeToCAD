from codetocad import *
from codetocad.shortcuts import *


material = Material("material")
material.set_color(169, 76, 181, 255)


def create_cube(name, size):
    calibartion_cube = Part.create_cube(size, size, size)

    calibration_cube_x = calibartion_cube.create_landmark(
        "x", min + "5mm", max - "7mm", max
    )
    calibration_cube_y = calibartion_cube.create_landmark(
        "y", "max-5mm", "min+5mm", max
    )
    calibration_cube_z = calibartion_cube.create_landmark("z", center, min, center)
    calibration_cube_size = calibartion_cube.create_landmark(
        "size", "min+1mm", "min+2mm", max
    )

    z = Sketch.create_text("Z^", "10mm").extrude("1.5mm").rotate_xyz(90, 0, 0)
    z_center = z.create_landmark("center", center, center, center)
    Joint(calibration_cube_z, z_center).limit_location_xyz(0, 0, 0)
    calibartion_cube.subtract(z)

    y = Sketch.create_text("Y^", "8mm").extrude("1.5mm")
    y_center = y.create_landmark("center", center, center, center)
    Joint(calibration_cube_y, y_center).limit_location_xyz(0, 0, 0)
    calibartion_cube.subtract(y)

    x = Sketch.create_text("X^", "8mm").extrude("1.5mm").rotate_xyz(180, 0, 90)
    x_center = x.create_landmark("center", center, center, center)
    Joint(calibration_cube_x, x_center).limit_location_xyz(0, 0, 0)
    calibartion_cube.subtract(x)

    size = Sketch.create_text(str(size.value) + "mm", "4mm").extrude("1.5mm")
    size_center = size.create_landmark("min", min, center, center)
    Joint(calibration_cube_size, size_center).limit_location_xyz(0, 0, 0)
    calibartion_cube.subtract(size)

    calibartion_cube.set_material(material)

    return calibartion_cube


tolerance = "0.2mm"
size = Dimension(20, "mm")

create_cube("calibration_cube19_9", size - tolerance).export(
    "./calibration_cube19_8mm.stl", scale=1000
).translate_xyz("-25mm", 0, 0)
create_cube("calibration_cube20mm", size).export(
    "./calibration_cube20mm.stl", scale=1000
)
create_cube("calibration_cube20_2", size + tolerance).export(
    "./calibration_cube20_2mm.stl", scale=1000
).translate_xyz("25mm", 0, 0)
