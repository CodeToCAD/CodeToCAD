# THIS IS AN AUTO-GENERATE FILE. 
# DO NOT EDIT MANUALLY.
# Please run development/capabilitiesJsonToPython/capabilitiesToPy.sh to generate this file.
# Copy this file and remove this header to create a new CodeToCAD Provider.

from typing import Optional

from CodeToCAD.interfaces import RenderInterface
from CodeToCAD.CodeToCADTypes import *
from CodeToCAD.utilities import *


class Render(RenderInterface): 
    
    

    def renderImage(self, outputFilePath:str, overwrite:bool=True, fileType:Optional[str]=None):
        
        return self
        

    def renderVideoMp4(self, outputFilePath:str, startFrameNumber:'int'=1, endFrameNumber:'int'=100, stepFrames:'int'=1, overwrite:bool=True):
        
        return self
        

    def renderVideoFrames(self, outputFolderPath:str, fileNamePrefix:str, startFrameNumber:'int'=1, endFrameNumber:'int'=100, stepFrames:'int'=1, overwrite:bool=True, fileType:Optional[str]=None):
        
        return self
        

    def setFrameRate(self, frameRate:'int'):
        
        return self
        

    def setResolution(self, x:'int', y:'int'):
        
        return self
        

    def setRenderQuality(self, quality:'int'):
        
        return self
        

    def setRenderEngine(self, name:str):
        
        return self
        

    def setCamera(self, cameraNameOrInstance:CameraOrItsName):
        
        return self
        
    