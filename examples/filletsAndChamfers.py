from codetocad import *

blueMaterial = Material("blue").setColor(0, 0.1, 1.0)
redMaterial = Material("red").setColor(1.0, 0.1, 0)

Part("filletAllEdges").createCube(1, 1, 1).filletAllEdges(
    "10cm").setMaterial(blueMaterial)
Part("chamferAllEdges").createCube(1, 1, 1).translateXYZ(
    1.5, 0, 0).setMaterial(redMaterial).chamferAllEdges("10cm")

Part("filletAllEdgesCylinder").createCylinder(1/2, 2).translateXYZ(1.5 *
                                                                   2, 0, 0).filletAllEdges("10cm").setMaterial(blueMaterial)
Part("chamferAllEdgesCylinder").createCylinder(1/2, 2).translateXYZ(1.5 *
                                                                    3, 0, 0).chamferAllEdges("10cm").setMaterial(redMaterial)

filletTwoEdges = Part("filletTwoEdges").createCube(1, 1, 1)
filletTwoEdges_edge1 = filletTwoEdges.createLandmark("edge1", max, 0, max)
filletTwoEdges_edge2 = filletTwoEdges.createLandmark("edge2", min, 0, min)
filletTwoEdges.filletEdges("10cm", [filletTwoEdges_edge1, filletTwoEdges_edge2]).translateXYZ(
    0, 1.5, 0).setMaterial(blueMaterial)

chamferTwoEdges = Part("chamferTwoEdges").createCube(1, 1, 1)
chamferTwoEdges_edge1 = chamferTwoEdges.createLandmark("edge1", max, 0, max)
chamferTwoEdges_edge2 = chamferTwoEdges.createLandmark("edge2", min, 0, min)
chamferTwoEdges.chamferEdges("10cm", [chamferTwoEdges_edge1, chamferTwoEdges_edge2]).translateXYZ(
    1.5, 1.5, 0).setMaterial(redMaterial)

filletTwoFaces = Part("filletTwoFaces").createCube(1, 1, 1)
filletTwoFaces_face1 = filletTwoFaces.createLandmark("face1", 0, 0, max)
filletTwoFaces_face2 = filletTwoFaces.createLandmark("face2", min, 0, 0)
filletTwoFaces.filletFaces("10cm", [filletTwoFaces_face1, filletTwoFaces_face2]).translateXYZ(
    1.5*2, 1.5, 0).setMaterial(blueMaterial)

chamferTwoFaces = Part("chamferTwoFaces").createCube(1, 1, 1)
chamferTwoFaces_face1 = chamferTwoFaces.createLandmark("face1", 0, 0, max)
chamferTwoFaces_face2 = chamferTwoFaces.createLandmark("face2", min, 0, 0)
chamferTwoFaces.chamferFaces("10cm", [chamferTwoFaces_face1, chamferTwoFaces_face2]).translateXYZ(
    1.5*3, 1.5, 0).setMaterial(redMaterial)
