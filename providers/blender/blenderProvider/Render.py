from typing import Optional

from . import BlenderActions
from . import BlenderDefinitions

from . import BlenderActions
from . import BlenderDefinitions

from codetocad.interfaces import RenderInterface, CameraInterface
from codetocad.codetocad_types import *
from codetocad.utilities import *


class Render(RenderInterface):

    @staticmethod
    def _setFileFormat(outputFilePath: str):
        fileFormat = BlenderDefinitions.FileFormat.fromUtilitiesFileFormat(
            FileFormats.fromString(getFileExtension(outputFilePath)))
        BlenderActions.setRenderFileFormat(fileFormat)

    def renderImage(self, outputFilePath: str, overwrite: bool = True, fileType: Optional[str] = None):

        absoluteFilePath = getAbsoluteFilepath(outputFilePath)

        Render._setFileFormat(absoluteFilePath)

        BlenderActions.renderImage(absoluteFilePath, overwrite or True)

        return self

    def renderVideoMp4(self, outputFilePath: str, startFrameNumber: 'int' = 1, endFrameNumber: 'int' = 100, stepFrames: 'int' = 1, overwrite: bool = True):

        absoluteFilePath = getAbsoluteFilepath(outputFilePath)

        Render._setFileFormat(absoluteFilePath)

        BlenderActions.renderAnimation(absoluteFilePath, overwrite or True)
        return self

    def renderVideoFrames(self, outputFolderPath: str, fileNamePrefix: str, startFrameNumber: 'int' = 1, endFrameNumber: 'int' = 100, stepFrames: 'int' = 1, overwrite: bool = True, fileType: Optional[str] = None):

        absoluteFilePath = getAbsoluteFilepath(outputFolderPath)

        raise NotImplementedError()
        return self

    def setFrameRate(self, frameRate: int):

        BlenderActions.setRenderFrameRate(int(frameRate))

        return self

    def setResolution(self, x: 'int', y: 'int'):
        BlenderActions.setRenderResolution(x, y)
        return self

    def setRenderQuality(self, quality: int):

        percentage = quality * 100 if quality < 1.0 else quality
        percentage = int(percentage)
        BlenderActions.setRenderQuality(percentage)

        return self

    def setRenderEngine(self, name: str):

        BlenderActions.setRenderEngine(
            BlenderDefinitions.RenderEngines.fromString(name))

        return self

    def setCamera(self, cameraNameOrInstance: CameraOrItsName):

        cameraName = cameraNameOrInstance
        if isinstance(cameraName, CameraInterface):
            cameraName = cameraName.name

        BlenderActions.setSceneCamera(cameraName)

        return self
