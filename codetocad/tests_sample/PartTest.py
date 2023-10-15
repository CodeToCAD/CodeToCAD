# THIS IS AN AUTO-GENERATE FILE. 
# DO NOT EDIT MANUALLY.
# Please run development/capabilitiesJsonToPython/capabilitiesToPy.sh to generate this file.

# testsSample will implement these interfaces - this ensures that as capabilities.json is updated, tests are up to date as well.

from unittest import skip

from .test_helper import *
from codetocad.testsInterfaces import PartTestInterface

class PartTest(TestProviderCase, PartTestInterface):
    
    @skip("TODO")
    def test_createCube(self):
        instance = Part("")

        value = instance.createCube("width","length","height","keywordArguments")

        
        assert value.isExists(), "Create method failed."
        
    @skip("TODO")
    def test_createCone(self):
        instance = Part("")

        value = instance.createCone("radius","height","draftRadius","keywordArguments")

        
        assert value.isExists(), "Create method failed."
        
    @skip("TODO")
    def test_createCylinder(self):
        instance = Part("")

        value = instance.createCylinder("radius","height","keywordArguments")

        
        assert value.isExists(), "Create method failed."
        
    @skip("TODO")
    def test_createTorus(self):
        instance = Part("")

        value = instance.createTorus("innerRadius","outerRadius","keywordArguments")

        
        assert value.isExists(), "Create method failed."
        
    @skip("TODO")
    def test_createSphere(self):
        instance = Part("")

        value = instance.createSphere("radius","keywordArguments")

        
        assert value.isExists(), "Create method failed."
        
    @skip("TODO")
    def test_createGear(self):
        instance = Part("")

        value = instance.createGear("outerRadius","addendum","innerRadius","dedendum","height","pressureAngle","numberOfTeeth","skewAngle","conicalAngle","crownAngle","keywordArguments")

        
        assert value.isExists(), "Create method failed."
        
    @skip("TODO")
    def test_clone(self):
        instance = Part("")

        value = instance.clone("newName","copyLandmarks")

        
        assert value, "Get method failed."
        
    @skip("TODO")
    def test_loft(self):
        instance = Part("")

        value = instance.loft("Landmark1","Landmark2")

        
        assert value.isExists(), "Create method failed."
        
    @skip("TODO")
    def test_union(self):
        instance = Part("")

        value = instance.union("withPart","deleteAfterUnion","isTransferLandmarks")

        
        assert value, "Modify method failed."
        
    @skip("TODO")
    def test_subtract(self):
        instance = Part("")

        value = instance.subtract("withPart","deleteAfterSubtract","isTransferLandmarks")

        
        assert value, "Modify method failed."
        
    @skip("TODO")
    def test_intersect(self):
        instance = Part("")

        value = instance.intersect("withPart","deleteAfterIntersect","isTransferLandmarks")

        
        assert value, "Modify method failed."
        
    @skip("TODO")
    def test_hollow(self):
        instance = Part("")

        value = instance.hollow("thicknessX","thicknessY","thicknessZ","startAxis","flipAxis")

        
        assert value, "Modify method failed."
        
    @skip("TODO")
    def test_thicken(self):
        instance = Part("")

        value = instance.thicken("radius")

        
        assert value, "Modify method failed."
        
    @skip("TODO")
    def test_hole(self):
        instance = Part("")

        value = instance.hole("holeLandmark","radius","depth","normalAxis","flipAxis","initialRotationX","initialRotationY","initialRotationZ","mirrorAboutEntityOrLandmark","mirrorAxis","mirror","circularPatternInstanceCount","circularPatternInstanceSeparation","circularPatternInstanceAxis","circularPatternAboutEntityOrLandmark","linearPatternInstanceCount","linearPatternInstanceSeparation","linearPatternInstanceAxis","linearPattern2ndInstanceCount","linearPattern2ndInstanceSeparation","linearPattern2ndInstanceAxis")

        
        assert value, "Modify method failed."
        
    @skip("TODO")
    def test_setMaterial(self):
        instance = Part("")

        value = instance.setMaterial("materialName")

        
        assert value, "Modify method failed."
        
    @skip("TODO")
    def test_isCollidingWithPart(self):
        instance = Part("")

        value = instance.isCollidingWithPart("otherPart")

        
        assert value, "Get method failed."
        
    @skip("TODO")
    def test_filletAllEdges(self):
        instance = Part("")

        value = instance.filletAllEdges("radius","useWidth")

        
        assert value, "Modify method failed."
        
    @skip("TODO")
    def test_filletEdges(self):
        instance = Part("")

        value = instance.filletEdges("radius","landmarksNearEdges","useWidth")

        
        assert value, "Modify method failed."
        
    @skip("TODO")
    def test_filletFaces(self):
        instance = Part("")

        value = instance.filletFaces("radius","landmarksNearFaces","useWidth")

        
        assert value, "Modify method failed."
        
    @skip("TODO")
    def test_chamferAllEdges(self):
        instance = Part("")

        value = instance.chamferAllEdges("radius")

        
        assert value, "Modify method failed."
        
    @skip("TODO")
    def test_chamferEdges(self):
        instance = Part("")

        value = instance.chamferEdges("radius","landmarksNearEdges")

        
        assert value, "Modify method failed."
        
    @skip("TODO")
    def test_chamferFaces(self):
        instance = Part("")

        value = instance.chamferFaces("radius","landmarksNearFaces")

        
        assert value, "Modify method failed."
        
    @skip("TODO")
    def test_selectVertexNearLandmark(self):
        instance = Part("")

        value = instance.selectVertexNearLandmark("landmarkName")

        
    @skip("TODO")
    def test_selectEdgeNearLandmark(self):
        instance = Part("")

        value = instance.selectEdgeNearLandmark("landmarkName")

        
    @skip("TODO")
    def test_selectFaceNearLandmark(self):
        instance = Part("")

        value = instance.selectFaceNearLandmark("landmarkName")

        