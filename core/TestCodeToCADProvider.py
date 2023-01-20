# THIS IS AN AUTO-GENERATE FILE. 
# DO NOT EDIT MANUALLY.
# Please run capabilitiesToPyTest.sh to generate this file.

from typing import Optional
import unittest

from CodeToCAD import *
import core.CodeToCADInterface as CodeToCADInterface
import core.utilities as Utilities
from core.utilities import (Angle, BoundaryBox, CurveTypes, Dimension,
                            Dimensions, Point, center, createUUID,
                            getAbsoluteFilepath, getFilename, max, min)

class TestEntity(unittest.TestCase):
    
    
    @unittest.skip
    def test_isExists(self):
        instance = Part("name","description")

        value = instance.isExists("")

        
        assert value, "Get method succeeded."
        
    @unittest.skip
    def test_rename(self):
        instance = Part("name","description")

        value = instance.rename("newName","renamelinkedEntitiesAndLandmarks")

        
        assert value, "Modify method succeeded."
        
    @unittest.skip
    def test_delete(self):
        instance = Part("name","description")

        value = instance.delete("removeChildren")

        
    @unittest.skip
    def test_isVisible(self):
        instance = Part("name","description")

        value = instance.isVisible("")

        
        assert value, "Get method succeeded."
        
    @unittest.skip
    def test_setVisible(self):
        instance = Part("name","description")

        value = instance.setVisible("isVisible")

        
    @unittest.skip
    def test_apply(self):
        instance = Part("name","description")

        value = instance.apply("")

        
        assert value, "Modify method succeeded."
        
    @unittest.skip
    def test_getNativeInstance(self):
        instance = Part("name","description")

        value = instance.getNativeInstance("")

        
        assert value, "Get method succeeded."
        
    @unittest.skip
    def test_getLocationWorld(self):
        instance = Part("name","description")

        value = instance.getLocationWorld("")

        
        assert value, "Get method succeeded."
        
    @unittest.skip
    def test_getLocationLocal(self):
        instance = Part("name","description")

        value = instance.getLocationLocal("")

        
        assert value, "Get method succeeded."
        
    @unittest.skip
    def test_select(self):
        instance = Part("name","description")

        value = instance.select("landmarkName","selectionType")

        
    @unittest.skip
    def test_export(self):
        instance = Part("name","description")

        value = instance.export("filePath","overwrite","scale")

        
    @unittest.skip
    def test_clone(self):
        instance = Part("name","description")

        value = instance.clone("newName","copyLandmarks")

        
        assert value.isExists(), "Create method failed."
        
    @unittest.skip
    def test_mirror(self):
        instance = Part("name","description")

        value = instance.mirror("mirrorAcrossEntity","axis","resultingMirroredEntityName")

        
        assert value.isExists(), "Create method failed."
        
    @unittest.skip
    def test_linearPattern(self):
        instance = Part("name","description")

        value = instance.linearPattern("instanceCount","directionAxis","offset")

        
        assert value.isExists(), "Create method failed."
        
    @unittest.skip
    def test_circularPattern(self):
        instance = Part("name","description")

        value = instance.circularPattern("instanceCount","separationAngle","normalDirectionAxis","centerEntityOrLandmark")

        
        assert value.isExists(), "Create method failed."
        
    @unittest.skip
    def test_scaleX(self):
        instance = Part("name","description")

        value = instance.scaleX("scale")

        
        assert value, "Modify method succeeded."
        
    @unittest.skip
    def test_scaleY(self):
        instance = Part("name","description")

        value = instance.scaleY("scale")

        
        assert value, "Modify method succeeded."
        
    @unittest.skip
    def test_scaleZ(self):
        instance = Part("name","description")

        value = instance.scaleZ("scale")

        
        assert value, "Modify method succeeded."
        
    @unittest.skip
    def test_scaleKeepAspectRatio(self):
        instance = Part("name","description")

        value = instance.scaleKeepAspectRatio("scale","axis")

        
        assert value, "Modify method succeeded."
        
    @unittest.skip
    def test_rotateX(self):
        instance = Part("name","description")

        value = instance.rotateX("rotation")

        
        assert value, "Modify method succeeded."
        
    @unittest.skip
    def test_rotateY(self):
        instance = Part("name","description")

        value = instance.rotateY("rotation")

        
        assert value, "Modify method succeeded."
        
    @unittest.skip
    def test_rotateZ(self):
        instance = Part("name","description")

        value = instance.rotateZ("rotation")

        
        assert value, "Modify method succeeded."
        
    @unittest.skip
    def test_twist(self):
        instance = Part("name","description")

        value = instance.twist("angle","screwPitch","interations","axis")

        
        assert value, "Modify method succeeded."
        
    @unittest.skip
    def test_remesh(self):
        instance = Part("name","description")

        value = instance.remesh("strategy","amount")

        
        assert value, "Modify method succeeded."
        
    @unittest.skip
    def test_createLandmark(self):
        instance = Part("name","description")

        value = instance.createLandmark("landmarkName","x","y","z")

        
        assert value, "Modify method succeeded."
        
    @unittest.skip
    def test_getBoundingBox(self):
        instance = Part("name","description")

        value = instance.getBoundingBox("")

        
        assert value, "Get method succeeded."
        
    @unittest.skip
    def test_getDimensions(self):
        instance = Part("name","description")

        value = instance.getDimensions("")

        
        assert value, "Get method succeeded."
        
    @unittest.skip
    def test_getLandmark(self):
        instance = Part("name","description")

        value = instance.getLandmark("landmarkName")

        
        assert value, "Get method succeeded."
        
class TestPart(unittest.TestCase):
    
    @unittest.skip
    def test_createFromFile(self):
        instance = Part("")

        value = instance.createFromFile("filePath","fileType")

        
        assert value.isExists(), "Create method failed."
        
    @unittest.skip
    def test_createPrimitive(self):
        instance = Part("")

        value = instance.createPrimitive("primitiveName","dimensions","keywordArguments")

        
        assert value.isExists(), "Create method failed."
        
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
    def test_loft(self):
        instance = Part("")

        value = instance.loft("Landmark1","Landmark2")

        
        assert value.isExists(), "Create method failed."
        
    @unittest.skip
    def test_union(self):
        instance = Part("")

        value = instance.union("withPart","deleteAfterUnion","isTransferLandmarks")

        
        assert value, "Modify method succeeded."
        
    @unittest.skip
    def test_subtract(self):
        instance = Part("")

        value = instance.subtract("withPart","deleteAfterUnion","isTransferLandmarks")

        
        assert value, "Modify method succeeded."
        
    @unittest.skip
    def test_intersect(self):
        instance = Part("")

        value = instance.intersect("withPart","deleteAfterUnion","isTransferLandmarks")

        
        assert value, "Modify method succeeded."
        
    @unittest.skip
    def test_hollow(self):
        instance = Part("")

        value = instance.hollow("thicknessX","thicknessY","thicknessZ","startAxis","flipAxis")

        
        assert value, "Modify method succeeded."
        
    @unittest.skip
    def test_hole(self):
        instance = Part("")

        value = instance.hole("holeLandmark","radius","depth","normalAxis","flip","instanceCount","instanceSeparation","aboutEntityOrLandmark","mirror","instanceAxis","initialRotationX","initialRotationY","initialRotationZ","leaveHoleEntity")

        
        assert value, "Modify method succeeded."
        
    @unittest.skip
    def test_assignMaterial(self):
        instance = Part("")

        value = instance.assignMaterial("materialName")

        
        assert value, "Modify method succeeded."
        
    @unittest.skip
    def test_isCollidingWithPart(self):
        instance = Part("")

        value = instance.isCollidingWithPart("otherPart")

        
        assert value, "Get method succeeded."
        
    @unittest.skip
    def test_filletAllEdges(self):
        instance = Part("")

        value = instance.filletAllEdges("radius","useWidth")

        
        assert value, "Modify method succeeded."
        
    @unittest.skip
    def test_filletEdges(self):
        instance = Part("")

        value = instance.filletEdges("radius","landmarksNearEdges","useWidth")

        
        assert value, "Modify method succeeded."
        
    @unittest.skip
    def test_filletFaces(self):
        instance = Part("")

        value = instance.filletFaces("radius","landmarksNearFaces","useWidth")

        
        assert value, "Modify method succeeded."
        
    @unittest.skip
    def test_chamferAllEdges(self):
        instance = Part("")

        value = instance.chamferAllEdges("radius")

        
        assert value, "Modify method succeeded."
        
    @unittest.skip
    def test_chamferEdges(self):
        instance = Part("")

        value = instance.chamferEdges("radius","landmarksNearEdges")

        
        assert value, "Modify method succeeded."
        
    @unittest.skip
    def test_chamferFaces(self):
        instance = Part("")

        value = instance.chamferFaces("radius","landmarksNearFaces")

        
        assert value, "Modify method succeeded."
        
class TestSketch(unittest.TestCase):
    
    
    @unittest.skip
    def test_revolve(self):
        instance = Sketch("name","curveType","description")

        value = instance.revolve("angle","aboutEntityOrLandmark","axis")

        
        assert value, "Modify method succeeded."
        
    @unittest.skip
    def test_extrude(self):
        instance = Sketch("name","curveType","description")

        value = instance.extrude("length","convertToMesh")

        
        assert value, "Modify method succeeded."
        
    @unittest.skip
    def test_sweep(self):
        instance = Sketch("name","curveType","description")

        value = instance.sweep("profileCurveName","fillCap")

        
        assert value, "Modify method succeeded."
        
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
        
class TestLandmark(unittest.TestCase):
    
    
    @unittest.skip
    def test_landmarkEntityName(self):
        instance = Landmark("name","parentEntity","description")

        value = instance.landmarkEntityName("")

        
        assert value, "Get method succeeded."
        
class TestJoint(unittest.TestCase):
    
    
    @unittest.skip
    def test_translateLandmarkOntoAnother(self):
        instance = Joint("entity1","entity2")

        value = instance.translateLandmarkOntoAnother("")

        
        assert value, "Modify method succeeded."
        
    @unittest.skip
    def test_pivot(self):
        instance = Joint("entity1","entity2")

        value = instance.pivot("")

        
        assert value, "Modify method succeeded."
        
    @unittest.skip
    def test_gearRatio(self):
        instance = Joint("entity1","entity2")

        value = instance.gearRatio("ratio")

        
        assert value, "Modify method succeeded."
        
    @unittest.skip
    def test_limitXLocation(self):
        instance = Joint("entity1","entity2")

        value = instance.limitXLocation("min","max")

        
        assert value, "Modify method succeeded."
        
    @unittest.skip
    def test_limitYLocation(self):
        instance = Joint("entity1","entity2")

        value = instance.limitYLocation("min","max")

        
        assert value, "Modify method succeeded."
        
    @unittest.skip
    def test_limitZLocation(self):
        instance = Joint("entity1","entity2")

        value = instance.limitZLocation("min","max")

        
        assert value, "Modify method succeeded."
        
    @unittest.skip
    def test_limitXRotation(self):
        instance = Joint("entity1","entity2")

        value = instance.limitXRotation("min","max")

        
        assert value, "Modify method succeeded."
        
    @unittest.skip
    def test_limitYRotation(self):
        instance = Joint("entity1","entity2")

        value = instance.limitYRotation("min","max")

        
        assert value, "Modify method succeeded."
        
    @unittest.skip
    def test_limitZRotation(self):
        instance = Joint("entity1","entity2")

        value = instance.limitZRotation("min","max")

        
        assert value, "Modify method succeeded."
        
class TestMaterial(unittest.TestCase):
    
    
    @unittest.skip
    def test_assignToPart(self):
        instance = Material("name","description")

        value = instance.assignToPart("partName")

        
        assert value, "Modify method succeeded."
        
    @unittest.skip
    def test_setColor(self):
        instance = Material("name","description")

        value = instance.setColor("rValue","gValue","bValue","aValue")

        
        assert value, "Modify method succeeded."
        
    @unittest.skip
    def test_addImageTexture(self):
        instance = Material("name","description")

        value = instance.addImageTexture("imageFilePath")

        
        assert value, "Modify method succeeded."
        
class TestAnimation(unittest.TestCase):
    
    
    
    @unittest.skip
    def test_createKeyFrameLocation(self):
        instance = Animation("")

        value = instance.createKeyFrameLocation("entity","frameNumber")

        
    @unittest.skip
    def test_createKeyFrameRotation(self):
        instance = Animation("")

        value = instance.createKeyFrameRotation("entity","frameNumber")

        
class TestScene(unittest.TestCase):
    
    
    
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

        
class TestAnalytics(unittest.TestCase):
    
    
    @unittest.skip
    def test_measureDistance(self):
        instance = Analytics("")

        value = instance.measureDistance("entity1","entity2")

        
        assert value, "Get method succeeded."
        
    @unittest.skip
    def test_measureAngle(self):
        instance = Analytics("")

        value = instance.measureAngle("entity1","entity2","pivot")

        
        assert value, "Get method succeeded."
        
    @unittest.skip
    def test_getWorldPose(self):
        instance = Analytics("")

        value = instance.getWorldPose("entity")

        
        assert value, "Get method succeeded."
        
    @unittest.skip
    def test_getBoundingBox(self):
        instance = Analytics("")

        value = instance.getBoundingBox("entityName")

        
        assert value, "Get method succeeded."
        
    @unittest.skip
    def test_getDimensions(self):
        instance = Analytics("")

        value = instance.getDimensions("entityName")

        
        assert value, "Get method succeeded."
        
