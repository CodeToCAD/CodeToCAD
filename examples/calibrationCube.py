from CodeToCAD import *


material = Material("material").setColor(169, 76, 181, 255)


def createCube(name, size):

    calibrationCube = Part(name).createCube(size, size, size)

    calibrationCube_x = calibrationCube.createLandmark(
        "x", "min+5mm", "max-5mm", max)
    calibrationCube_y = calibrationCube.createLandmark(
        "y", "max-5mm", "min+5mm", max)
    calibrationCube_z = calibrationCube.createLandmark(
        "z", center, min, center)
    calibrationCube_size = calibrationCube.createLandmark(
        "size", "min+1mm", "min+2mm", max)

    z = Sketch("Z").createText("Z^", "10mm").extrude("1.5mm").rotateXYZ(
        90, 0, 0)
    z_center = z.createLandmark("center", center, center, center)
    Joint(calibrationCube_z, z_center).limitLocationXYZ(0, 0, 0)
    calibrationCube.subtract(z, False)

    y = Sketch("Y").createText("Y^", "8mm").extrude(
        "1.5mm")
    y_center = y.createLandmark("center", center, center, center)
    Joint(calibrationCube_y, y_center).limitLocationXYZ(0, 0, 0)
    calibrationCube.subtract(y)

    x = Sketch("X").createText("X^", "8mm").extrude("1.5mm").rotateXYZ(
        180, 0, 90)
    x_center = x.createLandmark("center", center, center, center)
    Joint(calibrationCube_x, x_center).limitLocationXYZ(0, 0, 0)
    calibrationCube.subtract(x)

    size = Sketch("size").createText(str(size.value)+"mm",
                                     "4mm").extrude("1.5mm")
    size_center = size.createLandmark("min", min, center, center)
    Joint(calibrationCube_size, size_center).limitLocationXYZ(0, 0, 0)
    calibrationCube.subtract(size)

    calibrationCube.setMaterial(material)

    return calibrationCube


tolerance = "0.2mm"
size = Dimension(20, "mm")

createCube("CalibrationCube19_9", size - tolerance).export(
    "./calibrationCube19_8mm.stl", scale=1000).translateXYZ("-25mm", 0, 0)
# createCube("CalibrationCube20mm", size).export(
#     "./calibrationCube20mm.stl", scale=1000)
# createCube("CalibrationCube20_2", size + tolerance).export(
#     "./calibrationCube20_2mm.stl", scale=1000).translateXYZ("25mm", 0, 0)
