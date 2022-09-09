from CodeToCADBlenderProvider import *

blueMaterial = Material("blue").setColor(0,0.1,1.0)
redMaterial = Material("red").setColor(1.0,0.1,0)

Part("filletAllEdges").createCube(1,1,1).filletAllEdges("10cm").assignMaterial(blueMaterial)
Part("chamferAllEdges").createCube(1,1,1).translate(1.5,0,0).assignMaterial(redMaterial).chamferAllEdges("10cm")