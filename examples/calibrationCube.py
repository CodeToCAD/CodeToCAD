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

    z = Sketch("Z").createText("Z^", "10mm").extrude("1.5mm").rotate(
        90, 0, 0).createLandmark("center", center, center, center)
    Joint(calibrationCube_z, z).limitLocation(0, 0, 0)
    calibrationCube.subtract(z.localToEntityWithName)

    y = Sketch("Y").createText("Y^", "8mm").extrude(
        "1.5mm").createLandmark("center", center, center, center)
    Joint(calibrationCube_y, y).limitLocation(0, 0, 0)
    calibrationCube.subtract(y.localToEntityWithName)

    x = Sketch("X").createText("X^", "8mm").extrude("1.5mm").rotate(
        180, 0, 90).createLandmark("center", center, center, center)
    Joint(calibrationCube_x, x).limitLocation(0, 0, 0)
    calibrationCube.subtract(x.localToEntityWithName)

    size = Sketch("size").createText(str(size.value)+"mm",
                                     "4mm").extrude("1.5mm").createLandmark("min", min, center, center)
    Joint(calibrationCube_size, size).limitLocation(0, 0, 0)
    calibrationCube.subtract(size.localToEntityWithName)

    calibrationCube.setMaterial(material)

    return calibrationCube


tolerance = "0.2mm"
size = Dimension(20, "mm")

createCube("CalibrationCube19_9", size - tolerance).export(
    "./calibrationCube19_8mm.stl", scale=1000).translate("-25mm", 0, 0)
createCube("CalibrationCube20mm", size).export(
    "./calibrationCube20mm.stl", scale=1000)
createCube("CalibrationCube20_2", size + tolerance).export(
    "./calibrationCube20_2mm.stl", scale=1000).translate("25mm", 0, 0)
