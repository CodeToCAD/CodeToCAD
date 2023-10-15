from codetocad import *

redMaterial = Material("red").setColor(0.709804, 0.109394, 0.245126, 0.8)
blueMaterial = Material("blue").setColor(0.0865257, 0.102776, 0.709804, 0.8)
greenMaterial = Material("green").setColor(0.118213, 0.709804, 0.109477, 0.8)


a = Part("a").createCube(1, 1, 1).setMaterial(blueMaterial)
a_top = a.createLandmark("top", center, center, max)
a_bottom = a.createLandmark("bottom", center, center, min)

b = Part("b").createCube(1, 1, 1).setMaterial(redMaterial)
b_bottom = b.createLandmark("bottom", center, center, min)

c = Part("c").createCube(1, 1, 1).setMaterial(greenMaterial)
c_top = c.createLandmark("top", center, center, max)

# Joint("a","b","top","bottom").translateLandmarkOntoAnother()

Joint(a_top, b_bottom)\
    .limitLocationXYZ(0, 0, 0)\
    .limitRotationXYZ(0, 0, 0)

Joint(a_bottom, c_top)\
    .limitLocationXYZ(0, 0, 0)\
    .limitRotationXYZ(0, 0, 0)
