# THIS IS AN AUTO-GENERATE FILE. 
# DO NOT EDIT MANUALLY.
# Please run development/capabilitiesJsonToPython/capabilitiesToPy.sh to generate this file.

# testsSample will implement these interfaces - this ensures that as capabilities.json is updated, tests are up to date as well.

from unittest import skip

from .test_helper import *
from CodeToCAD.testsInterfaces import SketchTestInterface

class SketchTest(TestProviderCase, SketchTestInterface):
    
    
    @skip("TODO")
    def test_clone(self):
        instance = Sketch("name","curveType","description")

        value = instance.clone("newName","copyLandmarks")

        
        assert value, "Get method failed."
        
    @skip("TODO")
    def test_revolve(self):
        instance = Sketch("name","curveType","description")

        value = instance.revolve("angle","aboutEntityOrLandmark","axis")

        
        assert value, "Get method failed."
        
    @skip("TODO")
    def test_extrude(self):
        instance = Sketch("name","curveType","description")

        value = instance.extrude("length")

        
        assert value, "Get method failed."
        
    @skip("TODO")
    def test_sweep(self):
        instance = Sketch("name","curveType","description")

        value = instance.sweep("profileNameOrInstance","fillCap")

        
        assert value, "Get method failed."
        
    @skip("TODO")
    def test_offset(self):
        instance = Sketch("name","curveType","description")

        value = instance.offset("radius")

        
        assert value, "Modify method failed."
        
    @skip("TODO")
    def test_profile(self):
        instance = Sketch("name","curveType","description")

        value = instance.profile("profileCurveName")

        
        assert value, "Modify method failed."
        
    @skip("TODO")
    def test_createText(self):
        instance = Sketch("name","curveType","description")

        value = instance.createText("text","fontSize","bold","italic","underlined","characterSpacing","wordSpacing","lineSpacing","fontFilePath")

        
        assert value.isExists(), "Create method failed."
        
    @skip("TODO")
    def test_createFromVertices(self):
        instance = Sketch("name","curveType","description")

        value = instance.createFromVertices("coordinates","interpolation")

        
        assert value.isExists(), "Create method failed."
        
    @skip("TODO")
    def test_createPoint(self):
        instance = Sketch("name","curveType","description")

        value = instance.createPoint("coordinate")

        
        assert value.isExists(), "Create method failed."
        
    @skip("TODO")
    def test_createLine(self):
        instance = Sketch("name","curveType","description")

        value = instance.createLine("length","angleX","angleY","symmetric")

        
        assert value.isExists(), "Create method failed."
        
    @skip("TODO")
    def test_createLineBetweenPoints(self):
        instance = Sketch("name","curveType","description")

        value = instance.createLineBetweenPoints("endAt","startAt")

        
        assert value.isExists(), "Create method failed."
        
    @skip("TODO")
    def test_createCircle(self):
        instance = Sketch("name","curveType","description")

        value = instance.createCircle("radius")

        
        assert value.isExists(), "Create method failed."
        
    @skip("TODO")
    def test_createEllipse(self):
        instance = Sketch("name","curveType","description")

        value = instance.createEllipse("radiusA","radiusB")

        
        assert value.isExists(), "Create method failed."
        
    @skip("TODO")
    def test_createArc(self):
        instance = Sketch("name","curveType","description")

        value = instance.createArc("radius","angle")

        
        assert value.isExists(), "Create method failed."
        
    @skip("TODO")
    def test_createArcBetweenThreePoints(self):
        instance = Sketch("name","curveType","description")

        value = instance.createArcBetweenThreePoints("pointA","pointB","centerPoint")

        
        assert value.isExists(), "Create method failed."
        
    @skip("TODO")
    def test_createSegment(self):
        instance = Sketch("name","curveType","description")

        value = instance.createSegment("innerRadius","outerRadius","angle")

        
        assert value.isExists(), "Create method failed."
        
    @skip("TODO")
    def test_createRectangle(self):
        instance = Sketch("name","curveType","description")

        value = instance.createRectangle("length","width")

        
        assert value.isExists(), "Create method failed."
        
    @skip("TODO")
    def test_createPolygon(self):
        instance = Sketch("name","curveType","description")

        value = instance.createPolygon("numberOfSides","length","width")

        
        assert value.isExists(), "Create method failed."
        
    @skip("TODO")
    def test_createTrapezoid(self):
        instance = Sketch("name","curveType","description")

        value = instance.createTrapezoid("lengthUpper","lengthLower","height")

        
        assert value.isExists(), "Create method failed."
        
    @skip("TODO")
    def test_createSpiral(self):
        instance = Sketch("name","curveType","description")

        value = instance.createSpiral("numberOfTurns","height","radius","isClockwise","radiusEnd")

        
        assert value.isExists(), "Create method failed."
        