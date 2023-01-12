from CodeToCADBlenderProvider import *

material = Material("material").setColor(169, 76, 181, 0.8)
Part("Cube").createCube(1,1,1).assignMaterial(material)

materialWithTexture = Material("materialWithTexture").addImageTexture("./bark.jpg")
Part("Cylinder").createCylinder(1,4).assignMaterial(materialWithTexture).translate(5,0,0)