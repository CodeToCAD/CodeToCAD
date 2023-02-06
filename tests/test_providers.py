# This file was forked from core/TestCodeToCADProvider.py

from typing import Optional
import unittest

from mock.modeling.MockModelingProvider import resetMockModelingProvider, injectMockModelingProvider

from CodeToCAD import *
import core.CodeToCADInterface as CodeToCADInterface
import core.utilities as Utilities
from core.utilities import (Angle, BoundaryBox, CurveTypes, Dimension,
                            Dimensions, Point, center, createUUIDLikeId,
                            getAbsoluteFilepath, getFilename, max, min)

if __name__ == "__main__":
    print("Started test_provider")

    import tests.test_providers
    unittest.main(tests.test_providers)

    print("Completed test_provider")


def injectMockProvider():
    resetMockModelingProvider()
    injectMockModelingProvider(globals())


class TestEntity(unittest.TestCase):

    def setUp(self) -> None:
        injectMockProvider()
        super().setUp()

    def test_isExists(self):
        instance = Part("name", "description").createCube(1, 1, 1)

        value = instance.isExists()

        assert value, "Get method failed."

    def test_rename(self):
        instance = Part("name", "description").createCube(1, 1, 1)

        value = instance.rename("newName", True)

        renamedPart = Part("newName")

        assert value.name == renamedPart.name, "Modify method failed."

        # TODO: test for renamelinkedEntitiesAndLandmarks = False. This is blocked by landmarking implementation

    def test_delete(self):
        instance = Part("name", "description").createCube(1, 1, 1)

        value = instance.isExists()

        assert value, "Expected True, got False"

        value = instance.delete(False)

        value = instance.isExists()

        assert not value, "Expected False, got True"

        # TODO: test for removeChildren = True

    def test_isVisible(self):
        instance = Part("name", "description").createCube(1, 1, 1)

        value = instance.isVisible()

        assert value, "Get method failed."

    def test_setVisible(self):
        instance = Part("name", "description").createCube(1, 1, 1)

        value = instance.setVisible(True)

        assert value.isVisible() == True, "Expected False, got True"

        value = instance.setVisible(False)

        assert value.isVisible() == False, "Expected True, got False"

    @unittest.skip("Blocked by understanding the consequences of implementating this capability.")
    def test_apply(self):
        instance = Part("name", "description")

        value = instance.apply()

        assert value, "Modify method failed."

    def test_getNativeInstance(self):
        instance = Part("name", "description").createCube(1, 1, 1)

        value = instance.getNativeInstance()

        assert value, "Get method failed."

    def test_getLocationWorld(self):
        instance = Part("name", "description").createCube(1, 1, 1)

        value = instance.getLocationWorld()

        assert value.x == 0 and value.y == 0 and value.z == 0, "Get method failed."

        # TODO: get location world after translating

    def test_getLocationLocal(self):
        instance = Part("name", "description").createCube(1, 1, 1)

        value = instance.getLocationWorld()

        assert value.x == 0 and value.y == 0 and value.z == 0, "Get method failed."

        # TODO: get location world after translating

    @unittest.skip("Not yet implemented")
    def test_select(self):
        instance = Part("name", "description")

        value = instance.select("landmarkName", "selectionType")

    def test_export(self):
        instance = Part("name", "description").createCube(1, 1, 1)

        value = instance.export("filePath.stl", True, 1.0)

        # no extension:
        self.assertRaises(
            AssertionError, lambda: instance.export("filePath", True, 1.0))

        # bad extension:
        self.assertRaises(
            AssertionError, lambda: instance.export("filePath.NotARealExtension", True, 1.0))

        # TODO: Test file absolute path resolution
        # TODO: Test export scale
        # TODO: Test overwriting

    def test_clone(self):
        instance = Part("name", "description").createCube(1, 1, 1)

        value = instance.clone("newName", False)

        assert instance.isExists(), "The original object should still exist."

        assert instance.name == value.name, "Clone should not return the cloned Entity."

        assert Part("newName").isExists(), "Clone method failed."

        # TODO: test copyLandmarks parameter

    def test_mirror(self):
        partToMirror = Part("partToMirror", "description").createCube(
            1, 1, 1).translateX(-5)
        partToMirrorAcross = Part(
            "partToMirrorAcross", "description").createCube(1, 1, 1)

        value = partToMirror.mirror(partToMirrorAcross, "x", None)

        assert value.isExists(), "Create method failed."

        # TODO: add test for bad mirrorAcrossEntity name
        # TODO: add test for bad axis name
        # TODO: add test for supplying resultingMirroredEntityName
        # TODO: add test to make sure mirrored object is really mirrored across the intended axis and distance

    def test_linearPattern(self):
        instance = Part("name", "description").createCube(1, 1, 1)

        value = instance.linearPattern(
            2, "2m")

        assert value.isExists(), "Modify method failed."

        # TODO: make sure patterning works on all axes correctly

    def test_circularPattern(self):
        partToPattern = Part(
            "partToPattern", "description").createCube(1, 1, 1).translateX(-5)
        centerPart = Part("centerPart", "description").createCube(1, 1, 1)

        value = partToPattern.circularPattern(
            4, 90, centerPart)

        assert value.isExists(), "Modify method failed."

        # TODO: make sure Entity, Landmark and string name all work correctly.
        # TODO: make sure patterning works on all axes correctly

    def test_translateX(self):
        instance = Part("name", "description").createCube(1, 1, 1)

        value: Part = instance.translateX(5)

        assert value, "Modify method failed."

        assert instance.getLocationWorld() == Point(
            Dimension(5), Dimension(0), Dimension(0)), "Translation is not correct"

    def test_translateY(self):
        instance = Part("name", "description").createCube(1, 1, 1)

        value = instance.translateY(5)

        assert value, "Modify method failed."

        assert instance.getLocationWorld() == Point(
            Dimension(0), Dimension(5), Dimension(0)), "Translation is not correct"

    def test_translateZ(self):
        instance = Part("name", "description").createCube(1, 1, 1)

        value = instance.translateZ(5)

        assert value, "Modify method failed."

        assert instance.getLocationWorld() == Point(
            Dimension(0), Dimension(0), Dimension(5)), "Translation is not correct"

    def test_scaleX(self):
        instance = Part("name", "description").createCube(1, 1, 1)

        instance.scaleX(5)

        dimensions = instance.getDimensions()

        assert dimensions.x.value == 5 and dimensions.y.value == 1 and dimensions.z.value == 1, "Modify method failed."

    def test_scaleY(self):
        instance = Part("name", "description").createCube(1, 1, 1)

        instance.scaleY(5)

        dimensions = instance.getDimensions()

        assert dimensions.x.value == 1 and dimensions.y.value == 5 and dimensions.z.value == 1, "Modify method failed."

    def test_scaleZ(self):
        instance = Part("name", "description").createCube(1, 1, 1)

        instance.scaleZ(5)

        dimensions = instance.getDimensions()

        assert dimensions.x.value == 1 and dimensions.y.value == 1 and dimensions.z.value == 5, "Modify method failed."

    def test_scaleXByFactor(self):
        instance = Part("name", "description").createCube(1, 1, 1)

        instance.scaleXByFactor(5)

        dimensions = instance.getDimensions()

        assert dimensions.x.value == 5 and dimensions.y.value == 1 and dimensions.z.value == 1, "Modify method failed."

    def test_scaleYByFactor(self):
        instance = Part("name", "description").createCube(1, 1, 1)

        instance.scaleYByFactor(5)

        dimensions = instance.getDimensions()

        assert dimensions.x.value == 1 and dimensions.y.value == 5 and dimensions.z.value == 1, "Modify method failed."

    def test_scaleZByFactor(self):
        instance = Part("name", "description").createCube(1, 1, 1)

        instance.scaleZByFactor(5)

        dimensions = instance.getDimensions()

        assert dimensions.x.value == 1 and dimensions.y.value == 1 and dimensions.z.value == 5, "Modify method failed."

    def test_scaleKeepAspectRatio(self):
        instance = Part("name", "description").createCube(1, 1, 1)

        instance.scaleKeepAspectRatio(5, "x")

        dimensions = instance.getDimensions()

        assert dimensions.x.value == 5 and dimensions.y.value == 5 and dimensions.z.value == 5, "Modify method failed."

    def test_rotateX(self):
        instance = Part("name", "description").createCube(1, 1, 1)

        value = instance.rotateX(45)

        assert value, "Modify method failed."

    def test_rotateY(self):
        instance = Part("name", "description").createCube(1, 1, 1)

        value = instance.rotateY(45)

        assert value, "Modify method failed."

    def test_rotateZ(self):
        instance = Part("name", "description").createCube(1, 1, 1)

        value = instance.rotateZ(45)

        assert value, "Modify method failed."

    @unittest.skip
    def test_twist(self):
        instance = Part("name", "description")

        value = instance.twist("angle", "screwPitch", "interations", "axis")

        assert value, "Modify method failed."

    @unittest.skip
    def test_remesh(self):
        instance = Part("name", "description")

        value = instance.remesh("strategy", "amount")

        assert value, "Modify method failed."

    def test_createLandmark(self):
        instance = Part("name", "description").createCube(1, 1, 1)

        value = instance.createLandmark("landmarkName", 0, 0, 0)

        assert value, "Modify method failed."

        landmark = instance.getLandmark("landmarkName")

        assert landmark.isExists(), "Landmark was not created."

    @unittest.skip
    def test_getBoundingBox(self):
        instance = Part("name", "description")

        value = instance.getBoundingBox("")

        assert value, "Get method failed."

    @unittest.skip
    def test_getDimensions(self):
        instance = Part("name", "description")

        value = instance.getDimensions("")

        assert value, "Get method failed."

    @unittest.skip
    def test_getLandmark(self):
        instance = Part("name", "description")

        value = instance.getLandmark("landmarkName")

        assert value, "Get method failed."


class TestPart(unittest.TestCase):

    @unittest.skip
    def test_createFromFile(self):
        instance = Part("")

        value = instance.createFromFile("filePath", "fileType")

        assert value.isExists(), "Create method failed."

    @unittest.skip
    def test_createPrimitive(self):
        instance = Part("")

        value = instance.createPrimitive(
            "primitiveName", "dimensions", "keywordArguments")

        assert value.isExists(), "Create method failed."

    @unittest.skip
    def test_createCube(self):
        instance = Part("")

        value = instance.createCube(
            "width", "length", "height", "keywordArguments")

        assert value.isExists(), "Create method failed."

    @unittest.skip
    def test_createCone(self):
        instance = Part("")

        value = instance.createCone(
            "radius", "height", "draftRadius", "keywordArguments")

        assert value.isExists(), "Create method failed."

    @unittest.skip
    def test_createCylinder(self):
        instance = Part("")

        value = instance.createCylinder("radius", "height", "keywordArguments")

        assert value.isExists(), "Create method failed."

    @unittest.skip
    def test_createTorus(self):
        instance = Part("")

        value = instance.createTorus(
            "innerRadius", "outerRadius", "keywordArguments")

        assert value.isExists(), "Create method failed."

    @unittest.skip
    def test_createSphere(self):
        instance = Part("")

        value = instance.createSphere("radius", "keywordArguments")

        assert value.isExists(), "Create method failed."

    @unittest.skip
    def test_createGear(self):
        instance = Part("")

        value = instance.createGear("outerRadius", "addendum", "innerRadius", "dedendum", "height",
                                    "pressureAngle", "numberOfTeeth", "skewAngle", "conicalAngle", "crownAngle", "keywordArguments")

        assert value.isExists(), "Create method failed."

    @unittest.skip
    def test_loft(self):
        instance = Part("")

        value = instance.loft("Landmark1", "Landmark2")

        assert value.isExists(), "Create method failed."

    @unittest.skip
    def test_union(self):
        instance = Part("")

        value = instance.union(
            "withPart", "deleteAfterUnion", "isTransferLandmarks")

        assert value, "Modify method failed."

    @unittest.skip
    def test_subtract(self):
        instance = Part("")

        value = instance.subtract(
            "withPart", "deleteAfterUnion", "isTransferLandmarks")

        assert value, "Modify method failed."

    @unittest.skip
    def test_intersect(self):
        instance = Part("")

        value = instance.intersect(
            "withPart", "deleteAfterUnion", "isTransferLandmarks")

        assert value, "Modify method failed."

    @unittest.skip
    def test_hollow(self):
        instance = Part("")

        value = instance.hollow(
            "thicknessX", "thicknessY", "thicknessZ", "startAxis", "flipAxis")

        assert value, "Modify method failed."

    @unittest.skip
    def test_hole(self):
        instance = Part("")

        value = instance.hole("holeLandmark", "radius", "depth", "normalAxis", "flip", "instanceCount", "instanceSeparation",
                              "aboutEntityOrLandmark", "mirror", "instanceAxis", "initialRotationX", "initialRotationY", "initialRotationZ", "leaveHoleEntity")

        assert value, "Modify method failed."

    @unittest.skip
    def test_assignMaterial(self):
        instance = Part("")

        value = instance.assignMaterial("materialName")

        assert value, "Modify method failed."

    @unittest.skip
    def test_isCollidingWithPart(self):
        instance = Part("")

        value = instance.isCollidingWithPart("otherPart")

        assert value, "Get method failed."

    @unittest.skip
    def test_filletAllEdges(self):
        instance = Part("")

        value = instance.filletAllEdges("radius", "useWidth")

        assert value, "Modify method failed."

    @unittest.skip
    def test_filletEdges(self):
        instance = Part("")

        value = instance.filletEdges(
            "radius", "landmarksNearEdges", "useWidth")

        assert value, "Modify method failed."

    @unittest.skip
    def test_filletFaces(self):
        instance = Part("")

        value = instance.filletFaces(
            "radius", "landmarksNearFaces", "useWidth")

        assert value, "Modify method failed."

    @unittest.skip
    def test_chamferAllEdges(self):
        instance = Part("")

        value = instance.chamferAllEdges("radius")

        assert value, "Modify method failed."

    @unittest.skip
    def test_chamferEdges(self):
        instance = Part("")

        value = instance.chamferEdges("radius", "landmarksNearEdges")

        assert value, "Modify method failed."

    @unittest.skip
    def test_chamferFaces(self):
        instance = Part("")

        value = instance.chamferFaces("radius", "landmarksNearFaces")

        assert value, "Modify method failed."


class TestSketch(unittest.TestCase):

    @unittest.skip
    def test_revolve(self):
        instance = Sketch("name", "curveType", "description")

        value = instance.revolve("angle", "aboutEntityOrLandmark", "axis")

        assert value, "Modify method failed."

    @unittest.skip
    def test_extrude(self):
        instance = Sketch("name", "curveType", "description")

        value = instance.extrude("length", "convertToMesh")

        assert value, "Modify method failed."

    @unittest.skip
    def test_sweep(self):
        instance = Sketch("name", "curveType", "description")

        value = instance.sweep("profileCurveName", "fillCap")

        assert value, "Modify method failed."

    @unittest.skip
    def test_createText(self):
        instance = Sketch("name", "curveType", "description")

        value = instance.createText("text", "fontSize", "bold", "italic", "underlined",
                                    "characterSpacing", "wordSpacing", "lineSpacing", "fontFilePath")

        assert value.isExists(), "Create method failed."

    @unittest.skip
    def test_createFromVertices(self):
        instance = Sketch("name", "curveType", "description")

        value = instance.createFromVertices("coordinates", "interpolation")

        assert value.isExists(), "Create method failed."

    @unittest.skip
    def test_createPoint(self):
        instance = Sketch("name", "curveType", "description")

        value = instance.createPoint("coordinate")

        assert value.isExists(), "Create method failed."

    @unittest.skip
    def test_createLine(self):
        instance = Sketch("name", "curveType", "description")

        value = instance.createLine("length", "angleX", "angleY", "symmetric")

        assert value.isExists(), "Create method failed."

    @unittest.skip
    def test_createLineBetweenPoints(self):
        instance = Sketch("name", "curveType", "description")

        value = instance.createLineBetweenPoints("endAt", "startAt")

        assert value.isExists(), "Create method failed."

    @unittest.skip
    def test_createCircle(self):
        instance = Sketch("name", "curveType", "description")

        value = instance.createCircle("radius")

        assert value.isExists(), "Create method failed."

    @unittest.skip
    def test_createEllipse(self):
        instance = Sketch("name", "curveType", "description")

        value = instance.createEllipse("radiusA", "radiusB")

        assert value.isExists(), "Create method failed."

    @unittest.skip
    def test_createArc(self):
        instance = Sketch("name", "curveType", "description")

        value = instance.createArc("radius", "angle")

        assert value.isExists(), "Create method failed."

    @unittest.skip
    def test_createArcBetweenThreePoints(self):
        instance = Sketch("name", "curveType", "description")

        value = instance.createArcBetweenThreePoints(
            "pointA", "pointB", "centerPoint")

        assert value.isExists(), "Create method failed."

    @unittest.skip
    def test_createSegment(self):
        instance = Sketch("name", "curveType", "description")

        value = instance.createSegment("innerRadius", "outerRadius", "angle")

        assert value.isExists(), "Create method failed."

    @unittest.skip
    def test_createRectangle(self):
        instance = Sketch("name", "curveType", "description")

        value = instance.createRectangle("length", "width")

        assert value.isExists(), "Create method failed."

    @unittest.skip
    def test_createPolygon(self):
        instance = Sketch("name", "curveType", "description")

        value = instance.createPolygon("numberOfSides", "length", "width")

        assert value.isExists(), "Create method failed."

    @unittest.skip
    def test_createTrapezoid(self):
        instance = Sketch("name", "curveType", "description")

        value = instance.createTrapezoid(
            "lengthUpper", "lengthLower", "height")

        assert value.isExists(), "Create method failed."


class TestLandmark(unittest.TestCase):

    @unittest.skip
    def test_getLandmarkEntityName(self):
        instance = Landmark("name", "parentEntity", "description")

        value = instance.getLandmarkEntityName()

        assert value, "Get method failed."


class TestJoint(unittest.TestCase):

    @unittest.skip
    def test_translateLandmarkOntoAnother(self):
        instance = Joint("entity1", "entity2")

        value = instance.translateLandmarkOntoAnother("")

        assert value, "Modify method failed."

    @unittest.skip
    def test_pivot(self):
        instance = Joint("entity1", "entity2")

        value = instance.pivot("")

        assert value, "Modify method failed."

    @unittest.skip
    def test_gearRatio(self):
        instance = Joint("entity1", "entity2")

        value = instance.gearRatio("ratio")

        assert value, "Modify method failed."

    @unittest.skip
    def test_limitXLocation(self):
        instance = Joint("entity1", "entity2")

        value = instance.limitXLocation("min", "max")

        assert value, "Modify method failed."

    @unittest.skip
    def test_limitYLocation(self):
        instance = Joint("entity1", "entity2")

        value = instance.limitYLocation("min", "max")

        assert value, "Modify method failed."

    @unittest.skip
    def test_limitZLocation(self):
        instance = Joint("entity1", "entity2")

        value = instance.limitZLocation("min", "max")

        assert value, "Modify method failed."

    @unittest.skip
    def test_limitXRotation(self):
        instance = Joint("entity1", "entity2")

        value = instance.limitXRotation("min", "max")

        assert value, "Modify method failed."

    @unittest.skip
    def test_limitYRotation(self):
        instance = Joint("entity1", "entity2")

        value = instance.limitYRotation("min", "max")

        assert value, "Modify method failed."

    @unittest.skip
    def test_limitZRotation(self):
        instance = Joint("entity1", "entity2")

        value = instance.limitZRotation("min", "max")

        assert value, "Modify method failed."


class TestMaterial(unittest.TestCase):

    @unittest.skip
    def test_assignToPart(self):
        instance = Material("name", "description")

        value = instance.assignToPart("partName")

        assert value, "Modify method failed."

    @unittest.skip
    def test_setColor(self):
        instance = Material("name", "description")

        value = instance.setColor("rValue", "gValue", "bValue", "aValue")

        assert value, "Modify method failed."

    @unittest.skip
    def test_addImageTexture(self):
        instance = Material("name", "description")

        value = instance.addImageTexture("imageFilePath")

        assert value, "Modify method failed."


class TestAnimation(unittest.TestCase):

    @unittest.skip
    def test_createKeyFrameLocation(self):
        instance = Animation("")

        value = instance.createKeyFrameLocation("entity", "frameNumber")

    @unittest.skip
    def test_createKeyFrameRotation(self):
        instance = Animation("")

        value = instance.createKeyFrameRotation("entity", "frameNumber")


class TestScene(unittest.TestCase):

    @unittest.skip
    def test_create(self):
        instance = Scene("name", "description")

        value = instance.create("")

        assert value.isExists(), "Create method failed."

    @unittest.skip
    def test_delete(self):
        instance = Scene("name", "description")

        value = instance.delete("")

    @unittest.skip
    def test_export(self):
        instance = Scene("name", "description")

        value = instance.export("filePath", "entities", "overwrite", "scale")

    @unittest.skip
    def test_setDefaultUnit(self):
        instance = Scene("name", "description")

        value = instance.setDefaultUnit("unit")

    @unittest.skip
    def test_createGroup(self):
        instance = Scene("name", "description")

        value = instance.createGroup("name")

        assert value.isExists(), "Create method failed."

    @unittest.skip
    def test_deleteGroup(self):
        instance = Scene("name", "description")

        value = instance.deleteGroup("name", "removeChildren")

    @unittest.skip
    def test_removeFromGroup(self):
        instance = Scene("name", "description")

        value = instance.removeFromGroup("entityName", "groupName")

    @unittest.skip
    def test_assignToGroup(self):
        instance = Scene("name", "description")

        value = instance.assignToGroup(
            "entities", "groupName", "removeFromOtherGroups")

    @unittest.skip
    def test_setVisible(self):
        instance = Scene("name", "description")

        value = instance.setVisible("entities", "isVisible")


class TestAnalytics(unittest.TestCase):

    @unittest.skip
    def test_measureDistance(self):
        instance = Analytics("")

        value = instance.measureDistance("entity1", "entity2")

        assert value, "Get method failed."

    @unittest.skip
    def test_measureAngle(self):
        instance = Analytics("")

        value = instance.measureAngle("entity1", "entity2", "pivot")

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
