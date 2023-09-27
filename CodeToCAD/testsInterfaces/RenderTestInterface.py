# THIS IS AN AUTO-GENERATE FILE. 
# DO NOT EDIT MANUALLY.
# Please run development/capabilitiesJsonToPython/capabilitiesToPy.sh to generate this file.

# testsSample will implement these interfaces - this ensures that as capabilities.json is updated, tests are up to date as well.

from unittest import TestCase
from abc import ABCMeta, abstractmethod

from CodeToCAD import Render

class RenderTestInterface(TestCase, metaclass=ABCMeta):
    
    
    @abstractmethod
    def test_renderImage(self):
        instance = Render("")

        value = instance.renderImage("outputFilePath","overwrite","fileType")

        
    
    @abstractmethod
    def test_renderVideoMp4(self):
        instance = Render("")

        value = instance.renderVideoMp4("outputFilePath","startFrameNumber","endFrameNumber","stepFrames","overwrite")

        
    
    @abstractmethod
    def test_renderVideoFrames(self):
        instance = Render("")

        value = instance.renderVideoFrames("outputFolderPath","fileNamePrefix","startFrameNumber","endFrameNumber","stepFrames","overwrite","fileType")

        
    
    @abstractmethod
    def test_setFrameRate(self):
        instance = Render("")

        value = instance.setFrameRate("frameRate")

        
        assert value, "Modify method failed."
        
    
    @abstractmethod
    def test_setResolution(self):
        instance = Render("")

        value = instance.setResolution("x","y")

        
        assert value, "Modify method failed."
        
    
    @abstractmethod
    def test_setRenderQuality(self):
        instance = Render("")

        value = instance.setRenderQuality("quality")

        
        assert value, "Modify method failed."
        
    
    @abstractmethod
    def test_setRenderEngine(self):
        instance = Render("")

        value = instance.setRenderEngine("name")

        
        assert value, "Modify method failed."
        
    
    @abstractmethod
    def test_setCamera(self):
        instance = Render("")

        value = instance.setCamera("cameraNameOrInstance")

        
        assert value, "Modify method failed."
        