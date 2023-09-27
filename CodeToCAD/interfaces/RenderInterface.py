
# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilitiesJsonToPython/capabilitiesToPy.sh to generate this file.

from abc import ABCMeta, abstractmethod
from CodeToCAD.CodeToCADTypes import *


class RenderInterface(metaclass=ABCMeta):
    '''Render the scene and export images or videos.'''

    

    @abstractmethod
    def renderImage(self, outputFilePath:str, overwrite:bool=True, fileType:Optional[str]=None):
        '''
        Render a still image.
        '''
        
        print("renderImage is called in an abstract method. Please override this method.")
        return self
        

    @abstractmethod
    def renderVideoMp4(self, outputFilePath:str, startFrameNumber:'int'=1, endFrameNumber:'int'=100, stepFrames:'int'=1, overwrite:bool=True):
        '''
        Render an MP4 video.
        '''
        
        print("renderVideoMp4 is called in an abstract method. Please override this method.")
        return self
        

    @abstractmethod
    def renderVideoFrames(self, outputFolderPath:str, fileNamePrefix:str, startFrameNumber:'int'=1, endFrameNumber:'int'=100, stepFrames:'int'=1, overwrite:bool=True, fileType:Optional[str]=None):
        '''
        Render a video as image frame stills.
        '''
        
        print("renderVideoFrames is called in an abstract method. Please override this method.")
        return self
        

    @abstractmethod
    def setFrameRate(self, frameRate:'int'):
        '''
        Set rendering framerate.
        '''
        
        print("setFrameRate is called in an abstract method. Please override this method.")
        return self
        

    @abstractmethod
    def setResolution(self, x:'int', y:'int'):
        '''
        Set rendering resolution
        '''
        
        print("setResolution is called in an abstract method. Please override this method.")
        return self
        

    @abstractmethod
    def setRenderQuality(self, quality:'int'):
        '''
        Set rendering quality.
        '''
        
        print("setRenderQuality is called in an abstract method. Please override this method.")
        return self
        

    @abstractmethod
    def setRenderEngine(self, name:str):
        '''
        Set rendering engine name.
        '''
        
        print("setRenderEngine is called in an abstract method. Please override this method.")
        return self
        

    @abstractmethod
    def setCamera(self, cameraNameOrInstance:CameraOrItsName):
        '''
        Set the rendering camera.
        '''
        
        print("setCamera is called in an abstract method. Please override this method.")
        return self
        