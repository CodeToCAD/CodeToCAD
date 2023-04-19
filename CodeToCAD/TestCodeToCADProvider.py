# THIS IS AN AUTO-GENERATE FILE. 
# DO NOT EDIT MANUALLY.
# Please run development/capabilitiesJsonToPython/capabilitiesToPy.sh to generate this file.
# Copy this file and remove this header to create a new CodeToCAD Provider Test.

from typing import Optional
import unittest

from CodeToCAD import *
import CodeToCAD.CodeToCADInterface as CodeToCADInterface
import CodeToCAD.utilities as Utilities
from CodeToCAD.utilities import (Angle, BoundaryBox, CurveTypes, Dimension,
                            Dimensions, Point, center, createUUIDLikeId,
                            getAbsoluteFilepath, getFilename, max, min)

class TestProviderCase(unittest.TestCase):

    def setUp(self) -> None:
        # inject provider?
        super().setUp()

class TestEntity(TestProviderCase):
    
    
    @unittest.skip
    def test_createFromFile(self):
        instance = Part("name","description")

        value = instance.createFromFile("filePath","fileType")

        
        assert value.isExists(), "Create method failed."
        
    @unittest.skip
    def test_isExists(self):
        instance = Part("name","description")

        value = instance.isExists("")

        
        assert value, "Get method failed."
        
    @unittest.skip
    def test_rename(self):
        instance = Part("name","description")

        value = instance.rename("newName","renamelinkedEntitiesAndLandmarks")

        
        assert value, "Modify method failed."
        
    @unittest.skip
    def test_delete(self):
        instance = Part("name","description")

        value = instance.delete("removeChildren")

        
    @unittest.skip
    def test_isVisible(self):
        instance = Part("name","description")

        value = instance.isVisible("")

        
        assert value, "Get method failed."
        
    @unittest.skip
    def test_setVisible(self):
        instance = Part("name","description")

        value = instance.setVisible("isVisible")

        
    @unittest.skip
    def test_apply(self):
        instance = Part("name","description")

        value = instance.apply("")

        
        assert value, "Modify method failed."
        
    @unittest.skip
    def test_getNativeInstance(self):
        instance = Part("name","description")

        value = instance.getNativeInstance("")

        
        assert value, "Get method failed."
        
    @unittest.skip
    def test_getLocationWorld(self):
        instance = Part("name","description")

        value = instance.getLocationWorld("")

        
        assert value, "Get method failed."
        
    @unittest.skip
    def test_getLocationLocal(self):
        instance = Part("name","description")

        value = instance.getLocationLocal("")

        
        assert value, "Get method failed."
        
    @unittest.skip
    def test_select(self):
        instance = Part("name","description")

        value = instance.select("")

        
    @unittest.skip
    def test_export(self):
        instance = Part("name","description")

        value = instance.export("filePath","overwrite","scale")

        
    @unittest.skip
    def test_mirror(self):
        instance = Part("name","description")

        value = instance.mirror("mirrorAcrossEntityOrLandmark","axis","resultingMirroredEntityName")

        
        assert value.isExists(), "Create method failed."
        
    @unittest.skip
    def test_linearPattern(self):
        instance = Part("name","description")

        value = instance.linearPattern("instanceCount","offset","directionAxis")

        
        assert value, "Modify method failed."
        
    @unittest.skip
    def test_circularPattern(self):
        instance = Part("name","description")

        value = instance.circularPattern("instanceCount","separationAngle","centerEntityOrLandmark","normalDirectionAxis")

        
        assert value, "Modify method failed."
        
    @unittest.skip
    def test_translateXYZ(self):
        instance = Part("name","description")

        value = instance.translateXYZ("x","y","z")

        
        assert value, "Modify method failed."
        
    @unittest.skip
    def test_translateX(self):
        instance = Part("name","description")

        value = instance.translateX("amount")

        
        assert value, "Modify method failed."
        
    @unittest.skip
    def test_translateY(self):
        instance = Part("name","description")

        value = instance.translateY("amount")

        
        assert value, "Modify method failed."
        
    @unittest.skip
    def test_translateZ(self):
        instance = Part("name","description")

        value = instance.translateZ("amount")

        
        assert value, "Modify method failed."
        
    @unittest.skip
    def test_scaleXYZ(self):
        instance = Part("name","description")

        value = instance.scaleXYZ("x","y","z")

        
        assert value, "Modify method failed."
        
    @unittest.skip
    def test_scaleX(self):
        instance = Part("name","description")

        value = instance.scaleX("scale")

        
        assert value, "Modify method failed."
        
    @unittest.skip
    def test_scaleY(self):
        instance = Part("name","description")

        value = instance.scaleY("scale")

        
        assert value, "Modify method failed."
        
    @unittest.skip
    def test_scaleZ(self):
        instance = Part("name","description")

        value = instance.scaleZ("scale")

        
        assert value, "Modify method failed."
        
    @unittest.skip
    def test_scaleXByFactor(self):
        instance = Part("name","description")

        value = instance.scaleXByFactor("scaleFactor")

        
        assert value, "Modify method failed."
        
    @unittest.skip
    def test_scaleYByFactor(self):
        instance = Part("name","description")

        value = instance.scaleYByFactor("scaleFactor")

        
        assert value, "Modify method failed."
        
    @unittest.skip
    def test_scaleZByFactor(self):
        instance = Part("name","description")

        value = instance.scaleZByFactor("scaleFactor")

        
        assert value, "Modify method failed."
        
    @unittest.skip
    def test_scaleKeepAspectRatio(self):
        instance = Part("name","description")

        value = instance.scaleKeepAspectRatio("scale","axis")

        
        assert value, "Modify method failed."
        
    @unittest.skip
    def test_rotateXYZ(self):
        instance = Part("name","description")

        value = instance.rotateXYZ("x","y","z")

        
        assert value, "Modify method failed."
        
    @unittest.skip
    def test_rotateX(self):
        instance = Part("name","description")

        value = instance.rotateX("rotation")

        
        assert value, "Modify method failed."
        
    @unittest.skip
    def test_rotateY(self):
        instance = Part("name","description")

        value = instance.rotateY("rotation")

        
        assert value, "Modify method failed."
        
    @unittest.skip
    def test_rotateZ(self):
        instance = Part("name","description")

        value = instance.rotateZ("rotation")

        
        assert value, "Modify method failed."
        
    @unittest.skip
    def test_twist(self):
        instance = Part("name","description")

        value = instance.twist("angle","screwPitch","interations","axis")

        
        assert value, "Modify method failed."
        
    @unittest.skip
    def test_remesh(self):
        instance = Part("name","description")

        value = instance.remesh("strategy","amount")

        
        assert value, "Modify method failed."
        
    @unittest.skip
    def test_createLandmark(self):
        instance = Part("name","description")

        value = instance.createLandmark("landmarkName","x","y","z")

        
        assert value, "Get method failed."
        
    @unittest.skip
    def test_getBoundingBox(self):
        instance = Part("name","description")

        value = instance.getBoundingBox("")

        
        assert value, "Get method failed."
        
    @unittest.skip
    def test_getDimensions(self):
        instance = Part("name","description")

        value = instance.getDimensions("")

        
        assert value, "Get method failed."
        
    @unittest.skip
    def test_getLandmark(self):
        instance = Part("name","description")

        value = instance.getLandmark("landmarkName")

        
        assert value, "Get method failed."
        
class TestPart(TestProviderCase):
    
    @unittest.skip
    def test_createCube(self):
        instance = Part("")

        value = instance.createCube("width","length","height","keywordArguments")

        
        assert value.isExists(), "Create method failed."
        
    @unittest.skip
    def test_createCone(self):
        instance = Part("")

        value = instance.createCone("radius","height","draftRadius","keywordArguments")

        
        assert value.isExists(), "Create method failed."
        
    @unittest.skip
    def test_createCylinder(self):
        instance = Part("")

        value = instance.createCylinder("radius","height","keywordArguments")

        
        assert value.isExists(), "Create method failed."
        
    @unittest.skip
    def test_createTorus(self):
        instance = Part("")

        value = instance.createTorus("innerRadius","outerRadius","keywordArguments")

        
        assert value.isExists(), "Create method failed."
        
    @unittest.skip
    def test_createSphere(self):
        instance = Part("")

        value = instance.createSphere("radius","keywordArguments")

        
        assert value.isExists(), "Create method failed."
        
    @unittest.skip
    def test_createGear(self):
        instance = Part("")

        value = instance.createGear("outerRadius","addendum","innerRadius","dedendum","height","pressureAngle","numberOfTeeth","skewAngle","conicalAngle","crownAngle","keywordArguments")

        
        assert value.isExists(), "Create method failed."
        
    @unittest.skip
    def test_clone(self):
        instance = Part("")

        value = instance.clone("newName","copyLandmarks")

        
        assert value, "Get method failed."
        
    @unittest.skip
    def test_loft(self):
        instance = Part("")

        value = instance.loft("Landmark1","Landmark2")

        
        assert value.isExists(), "Create method failed."
        
    @unittest.skip
    def test_union(self):
        instance = Part("")

        value = instance.union("withPart","deleteAfterUnion","isTransferLandmarks")

        
        assert value, "Modify method failed."
        
    @unittest.skip
    def test_subtract(self):
        instance = Part("")

        value = instance.subtract("withPart","deleteAfterSubtract","isTransferLandmarks")

        
        assert value, "Modify method failed."
        
    @unittest.skip
    def test_intersect(self):
        instance = Part("")

        value = instance.intersect("withPart","deleteAfterIntersect","isTransferLandmarks")

        
        assert value, "Modify method failed."
        
    @unittest.skip
    def test_hollow(self):
        instance = Part("")

        value = instance.hollow("thicknessX","thicknessY","thicknessZ","startAxis","flipAxis")

        
        assert value, "Modify method failed."
        
    @unittest.skip
    def test_hole(self):
        instance = Part("")

        value = instance.hole("holeLandmark","radius","depth","normalAxis","flipAxis","initialRotationX","initialRotationY","initialRotationZ","mirrorAboutEntityOrLandmark","mirrorAxis","mirror","circularPatternInstanceCount","circularPatternInstanceSeparation","circularPatternInstanceAxis","circularPatternAboutEntityOrLandmark","linearPatternInstanceCount","linearPatternInstanceSeparation","linearPatternInstanceAxis")

        
        assert value, "Modify method failed."
        
    @unittest.skip
    def test_setMaterial(self):
        instance = Part("")

        value = instance.setMaterial("materialName")

        
        assert value, "Modify method failed."
        
    @unittest.skip
    def test_isCollidingWithPart(self):
        instance = Part("")

        value = instance.isCollidingWithPart("otherPart")

        
        assert value, "Get method failed."
        
    @unittest.skip
    def test_filletAllEdges(self):
        instance = Part("")

        value = instance.filletAllEdges("radius","useWidth")

        
        assert value, "Modify method failed."
        
    @unittest.skip
    def test_filletEdges(self):
        instance = Part("")

        value = instance.filletEdges("radius","landmarksNearEdges","useWidth")

        
        assert value, "Modify method failed."
        
    @unittest.skip
    def test_filletFaces(self):
        instance = Part("")

        value = instance.filletFaces("radius","landmarksNearFaces","useWidth")

        
        assert value, "Modify method failed."
        
    @unittest.skip
    def test_chamferAllEdges(self):
        instance = Part("")

        value = instance.chamferAllEdges("radius")

        
        assert value, "Modify method failed."
        
    @unittest.skip
    def test_chamferEdges(self):
        instance = Part("")

        value = instance.chamferEdges("radius","landmarksNearEdges")

        
        assert value, "Modify method failed."
        
    @unittest.skip
    def test_chamferFaces(self):
        instance = Part("")

        value = instance.chamferFaces("radius","landmarksNearFaces")

        
        assert value, "Modify method failed."
        
    @unittest.skip
    def test_selectVertexNearLandmark(self):
        instance = Part("")

        value = instance.selectVertexNearLandmark("landmarkName")

        
    @unittest.skip
    def test_selectEdgeNearLandmark(self):
        instance = Part("")

        value = instance.selectEdgeNearLandmark("landmarkName")

        
    @unittest.skip
    def test_selectFaceNearLandmark(self):
        instance = Part("")

        value = instance.selectFaceNearLandmark("landmarkName")

        
class TestSketch(TestProviderCase):
    
    
    @unittest.skip
    def test_clone(self):
        instance = Sketch("name","curveType","description")

        value = instance.clone("newName","copyLandmarks")

        
        assert value, "Get method failed."
        
    @unittest.skip
    def test_revolve(self):
        instance = Sketch("name","curveType","description")

        value = instance.revolve("angle","aboutEntityOrLandmark","axis")

        
        assert value, "Modify method failed."
        
    @unittest.skip
    def test_thicken(self):
        instance = Sketch("name","curveType","description")

        value = instance.thicken("radius")

        
        assert value, "Modify method failed."
        
    @unittest.skip
    def test_extrude(self):
        instance = Sketch("name","curveType","description")

        value = instance.extrude("length")

        
        assert value, "Get method failed."
        
    @unittest.skip
    def test_sweep(self):
        instance = Sketch("name","curveType","description")

        value = instance.sweep("profileCurveName","fillCap")

        
        assert value, "Modify method failed."
        
    @unittest.skip
    def test_profile(self):
        instance = Sketch("name","curveType","description")

        value = instance.profile("profileCurveName")

        
        assert value, "Modify method failed."
        
    @unittest.skip
    def test_createText(self):
        instance = Sketch("name","curveType","description")

        value = instance.createText("text","fontSize","bold","italic","underlined","characterSpacing","wordSpacing","lineSpacing","fontFilePath")

        
        assert value.isExists(), "Create method failed."
        
    @unittest.skip
    def test_createFromVertices(self):
        instance = Sketch("name","curveType","description")

        value = instance.createFromVertices("coordinates","interpolation")

        
        assert value.isExists(), "Create method failed."
        
    @unittest.skip
    def test_createPoint(self):
        instance = Sketch("name","curveType","description")

        value = instance.createPoint("coordinate")

        
        assert value.isExists(), "Create method failed."
        
    @unittest.skip
    def test_createLine(self):
        instance = Sketch("name","curveType","description")

        value = instance.createLine("length","angleX","angleY","symmetric")

        
        assert value.isExists(), "Create method failed."
        
    @unittest.skip
    def test_createLineBetweenPoints(self):
        instance = Sketch("name","curveType","description")

        value = instance.createLineBetweenPoints("endAt","startAt")

        
        assert value.isExists(), "Create method failed."
        
    @unittest.skip
    def test_createCircle(self):
        instance = Sketch("name","curveType","description")

        value = instance.createCircle("radius")

        
        assert value.isExists(), "Create method failed."
        
    @unittest.skip
    def test_createEllipse(self):
        instance = Sketch("name","curveType","description")

        value = instance.createEllipse("radiusA","radiusB")

        
        assert value.isExists(), "Create method failed."
        
    @unittest.skip
    def test_createArc(self):
        instance = Sketch("name","curveType","description")

        value = instance.createArc("radius","angle")

        
        assert value.isExists(), "Create method failed."
        
    @unittest.skip
    def test_createArcBetweenThreePoints(self):
        instance = Sketch("name","curveType","description")

        value = instance.createArcBetweenThreePoints("pointA","pointB","centerPoint")

        
        assert value.isExists(), "Create method failed."
        
    @unittest.skip
    def test_createSegment(self):
        instance = Sketch("name","curveType","description")

        value = instance.createSegment("innerRadius","outerRadius","angle")

        
        assert value.isExists(), "Create method failed."
        
    @unittest.skip
    def test_createRectangle(self):
        instance = Sketch("name","curveType","description")

        value = instance.createRectangle("length","width")

        
        assert value.isExists(), "Create method failed."
        
    @unittest.skip
    def test_createPolygon(self):
        instance = Sketch("name","curveType","description")

        value = instance.createPolygon("numberOfSides","length","width")

        
        assert value.isExists(), "Create method failed."
        
    @unittest.skip
    def test_createTrapezoid(self):
        instance = Sketch("name","curveType","description")

        value = instance.createTrapezoid("lengthUpper","lengthLower","height")

        
        assert value.isExists(), "Create method failed."
        
class TestLandmark(TestProviderCase):
    
    
    @unittest.skip
    def test_getLandmarkEntityName(self):
        instance = Landmark("name","parentEntity","description")

        value = instance.getLandmarkEntityName("")

        
        assert value, "Get method failed."
        
    @unittest.skip
    def test_getParentEntity(self):
        instance = Landmark("name","parentEntity","description")

        value = instance.getParentEntity("")

        
        assert value, "Get method failed."
        
    @unittest.skip
    def test_isExists(self):
        instance = Landmark("name","parentEntity","description")

        value = instance.isExists("")

        
        assert value, "Get method failed."
        
    @unittest.skip
    def test_rename(self):
        instance = Landmark("name","parentEntity","description")

        value = instance.rename("newName")

        
        assert value, "Modify method failed."
        
    @unittest.skip
    def test_delete(self):
        instance = Landmark("name","parentEntity","description")

        value = instance.delete("")

        
    @unittest.skip
    def test_isVisible(self):
        instance = Landmark("name","parentEntity","description")

        value = instance.isVisible("")

        
        assert value, "Get method failed."
        
    @unittest.skip
    def test_setVisible(self):
        instance = Landmark("name","parentEntity","description")

        value = instance.setVisible("isVisible")

        
    @unittest.skip
    def test_getNativeInstance(self):
        instance = Landmark("name","parentEntity","description")

        value = instance.getNativeInstance("")

        
        assert value, "Get method failed."
        
    @unittest.skip
    def test_getLocationWorld(self):
        instance = Landmark("name","parentEntity","description")

        value = instance.getLocationWorld("")

        
        assert value, "Get method failed."
        
    @unittest.skip
    def test_getLocationLocal(self):
        instance = Landmark("name","parentEntity","description")

        value = instance.getLocationLocal("")

        
        assert value, "Get method failed."
        
    @unittest.skip
    def test_select(self):
        instance = Landmark("name","parentEntity","description")

        value = instance.select("")

        
class TestJoint(TestProviderCase):
    
    
    @unittest.skip
    def test_translateLandmarkOntoAnother(self):
        instance = Joint("entity1","entity2")

        value = instance.translateLandmarkOntoAnother("")

        
        assert value, "Modify method failed."
        
    @unittest.skip
    def test_pivot(self):
        instance = Joint("entity1","entity2")

        value = instance.pivot("")

        
        assert value, "Modify method failed."
        
    @unittest.skip
    def test_gearRatio(self):
        instance = Joint("entity1","entity2")

        value = instance.gearRatio("ratio")

        
        assert value, "Modify method failed."
        
    @unittest.skip
    def test_limitLocationXYZ(self):
        instance = Joint("entity1","entity2")

        value = instance.limitLocationXYZ("x","y","z")

        
        assert value, "Modify method failed."
        
    @unittest.skip
    def test_limitLocationX(self):
        instance = Joint("entity1","entity2")

        value = instance.limitLocationX("min","max")

        
        assert value, "Modify method failed."
        
    @unittest.skip
    def test_limitLocationY(self):
        instance = Joint("entity1","entity2")

        value = instance.limitLocationY("min","max")

        
        assert value, "Modify method failed."
        
    @unittest.skip
    def test_limitLocationZ(self):
        instance = Joint("entity1","entity2")

        value = instance.limitLocationZ("min","max")

        
        assert value, "Modify method failed."
        
    @unittest.skip
    def test_limitRotationXYZ(self):
        instance = Joint("entity1","entity2")

        value = instance.limitRotationXYZ("x","y","z")

        
        assert value, "Modify method failed."
        
    @unittest.skip
    def test_limitRotationX(self):
        instance = Joint("entity1","entity2")

        value = instance.limitRotationX("min","max")

        
        assert value, "Modify method failed."
        
    @unittest.skip
    def test_limitRotationY(self):
        instance = Joint("entity1","entity2")

        value = instance.limitRotationY("min","max")

        
        assert value, "Modify method failed."
        
    @unittest.skip
    def test_limitRotationZ(self):
        instance = Joint("entity1","entity2")

        value = instance.limitRotationZ("min","max")

        
        assert value, "Modify method failed."
        
class TestMaterial(TestProviderCase):
    
    
    @unittest.skip
    def test_assignToPart(self):
        instance = Material("name","description")

        value = instance.assignToPart("partName")

        
        assert value, "Modify method failed."
        
    @unittest.skip
    def test_setColor(self):
        instance = Material("name","description")

        value = instance.setColor("rValue","gValue","bValue","aValue")

        
        assert value, "Modify method failed."
        
    @unittest.skip
    def test_addImageTexture(self):
        instance = Material("name","description")

        value = instance.addImageTexture("imageFilePath")

        
        assert value, "Modify method failed."
        
class TestAnimation(TestProviderCase):
    
    
    
    @unittest.skip
    def test_createKeyFrameLocation(self):
        instance = Animation("")

        value = instance.createKeyFrameLocation("entity","frameNumber")

        
    @unittest.skip
    def test_createKeyFrameRotation(self):
        instance = Animation("")

        value = instance.createKeyFrameRotation("entity","frameNumber")

        
class TestLight(TestProviderCase):
    
    @unittest.skip
    def test_setColor(self):
        instance = Light("name","description")

        value = instance.setColor("rValue","gValue","bValue")

        
        assert value, "Modify method failed."
        
    @unittest.skip
    def test_createSun(self):
        instance = Light("name","description")

        value = instance.createSun("energyLevel")

        
        assert value.isExists(), "Create method failed."
        
    @unittest.skip
    def test_createSpot(self):
        instance = Light("name","description")

        value = instance.createSpot("energyLevel")

        
        assert value.isExists(), "Create method failed."
        
    @unittest.skip
    def test_createPoint(self):
        instance = Light("name","description")

        value = instance.createPoint("energyLevel")

        
        assert value.isExists(), "Create method failed."
        
    @unittest.skip
    def test_createArea(self):
        instance = Light("name","description")

        value = instance.createArea("energyLevel")

        
        assert value.isExists(), "Create method failed."
        
    @unittest.skip
    def test_translateXYZ(self):
        instance = Light("name","description")

        value = instance.translateXYZ("x","y","z")

        
        assert value, "Modify method failed."
        
    @unittest.skip
    def test_rotateXYZ(self):
        instance = Light("name","description")

        value = instance.rotateXYZ("x","y","z")

        
        assert value, "Modify method failed."
        
    @unittest.skip
    def test_isExists(self):
        instance = Light("name","description")

        value = instance.isExists("")

        
        assert value, "Get method failed."
        
    @unittest.skip
    def test_rename(self):
        instance = Light("name","description")

        value = instance.rename("newName")

        
        assert value, "Modify method failed."
        
    @unittest.skip
    def test_delete(self):
        instance = Light("name","description")

        value = instance.delete("")

        
    @unittest.skip
    def test_getNativeInstance(self):
        instance = Light("name","description")

        value = instance.getNativeInstance("")

        
        assert value, "Get method failed."
        
    @unittest.skip
    def test_getLocationWorld(self):
        instance = Light("name","description")

        value = instance.getLocationWorld("")

        
        assert value, "Get method failed."
        
    @unittest.skip
    def test_getLocationLocal(self):
        instance = Light("name","description")

        value = instance.getLocationLocal("")

        
        assert value, "Get method failed."
        
    @unittest.skip
    def test_select(self):
        instance = Light("name","description")

        value = instance.select("")

        
class TestCamera(TestProviderCase):
    
    @unittest.skip
    def test_createPerspective(self):
        instance = Camera("name","description")

        value = instance.createPerspective("")

        
        assert value.isExists(), "Create method failed."
        
    @unittest.skip
    def test_createOrthogonal(self):
        instance = Camera("name","description")

        value = instance.createOrthogonal("")

        
        assert value.isExists(), "Create method failed."
        
    @unittest.skip
    def test_setFocalLength(self):
        instance = Camera("name","description")

        value = instance.setFocalLength("length")

        
        assert value, "Modify method failed."
        
    @unittest.skip
    def test_translateXYZ(self):
        instance = Camera("name","description")

        value = instance.translateXYZ("x","y","z")

        
        assert value, "Modify method failed."
        
    @unittest.skip
    def test_rotateXYZ(self):
        instance = Camera("name","description")

        value = instance.rotateXYZ("x","y","z")

        
        assert value, "Modify method failed."
        
    @unittest.skip
    def test_isExists(self):
        instance = Camera("name","description")

        value = instance.isExists("")

        
        assert value, "Get method failed."
        
    @unittest.skip
    def test_rename(self):
        instance = Camera("name","description")

        value = instance.rename("newName")

        
        assert value, "Modify method failed."
        
    @unittest.skip
    def test_delete(self):
        instance = Camera("name","description")

        value = instance.delete("")

        
    @unittest.skip
    def test_getNativeInstance(self):
        instance = Camera("name","description")

        value = instance.getNativeInstance("")

        
        assert value, "Get method failed."
        
    @unittest.skip
    def test_getLocationWorld(self):
        instance = Camera("name","description")

        value = instance.getLocationWorld("")

        
        assert value, "Get method failed."
        
    @unittest.skip
    def test_getLocationLocal(self):
        instance = Camera("name","description")

        value = instance.getLocationLocal("")

        
        assert value, "Get method failed."
        
    @unittest.skip
    def test_select(self):
        instance = Camera("name","description")

        value = instance.select("")

        
class TestScene(TestProviderCase):
    
    
    
    @unittest.skip
    def test_create(self):
        instance = Scene("name","description")

        value = instance.create("")

        
        assert value.isExists(), "Create method failed."
        
    @unittest.skip
    def test_delete(self):
        instance = Scene("name","description")

        value = instance.delete("")

        
    @unittest.skip
    def test_export(self):
        instance = Scene("name","description")

        value = instance.export("filePath","entities","overwrite","scale")

        
    @unittest.skip
    def test_setDefaultUnit(self):
        instance = Scene("name","description")

        value = instance.setDefaultUnit("unit")

        
    @unittest.skip
    def test_createGroup(self):
        instance = Scene("name","description")

        value = instance.createGroup("name")

        
        assert value.isExists(), "Create method failed."
        
    @unittest.skip
    def test_deleteGroup(self):
        instance = Scene("name","description")

        value = instance.deleteGroup("name","removeChildren")

        
    @unittest.skip
    def test_removeFromGroup(self):
        instance = Scene("name","description")

        value = instance.removeFromGroup("entityName","groupName")

        
    @unittest.skip
    def test_assignToGroup(self):
        instance = Scene("name","description")

        value = instance.assignToGroup("entities","groupName","removeFromOtherGroups")

        
    @unittest.skip
    def test_setVisible(self):
        instance = Scene("name","description")

        value = instance.setVisible("entities","isVisible")

        
    @unittest.skip
    def test_setBackgroundImage(self):
        instance = Scene("name","description")

        value = instance.setBackgroundImage("filePath","locationX","locationY")

        
        assert value, "Modify method failed."
        
class TestAnalytics(TestProviderCase):
    
    
    @unittest.skip
    def test_measureDistance(self):
        instance = Analytics("")

        value = instance.measureDistance("entity1","entity2")

        
        assert value, "Get method failed."
        
    @unittest.skip
    def test_measureAngle(self):
        instance = Analytics("")

        value = instance.measureAngle("entity1","entity2","pivot")

        
        assert value, "Get method failed."
        
    @unittest.skip
    def test_getWorldPose(self):
        instance = Analytics("")

        value = instance.getWorldPose("entity")

        
        assert value, "Get method failed."
        
    @unittest.skip
    def test_getBoundingBox(self):
        instance = Analytics("")

        value = instance.getBoundingBox("entityName")

        
        assert value, "Get method failed."
        
    @unittest.skip
    def test_getDimensions(self):
        instance = Analytics("")

        value = instance.getDimensions("entityName")

        
        assert value, "Get method failed."
        
