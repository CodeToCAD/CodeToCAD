from CodeToCADBlenderProvider import *

material = Material("material").setColor(169, 76, 181, 0.8)
Part("Cube").createCube(1,1,1).assignMaterial(material)