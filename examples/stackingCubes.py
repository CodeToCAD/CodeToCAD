from CodeToCAD import *

a = Part("a").createCube(1, 1, 1)
a_top = a.createLandmark("top", center, center, max)
a_bottom = a.createLandmark("bottom", center, center, min)

b = Part("b").createCube(1, 1, 1)
b_bottom = b.createLandmark("bottom", center, center, min)

c = Part("c").createCube(1, 1, 1)
c_top = c.createLandmark("top", center, center, max)

# Joint("a","b","top","bottom").translateLandmarkOntoAnother()

Joint("a", "b", "top", "bottom")\
    .limitLocation(0, 0, 0)\
    .limitRotation(0, 0, 0)

Joint(a, c, a_bottom, c_top)\
    .limitLocation(0, 0, 0)\
    .limitRotation(0, 0, 0)
