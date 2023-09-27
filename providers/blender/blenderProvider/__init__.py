# THIS IS AN AUTO-GENERATED FILE. DO NOT CHANGE.

from typing import Optional
from . import BlenderActions, BlenderDefinitions
from .Entity import Entity
from .Part import Part
from .Sketch import Sketch
from .Landmark import Landmark
from .Joint import Joint
from .Material import Material
from .Animation import Animation
from .Light import Light
from .Camera import Camera
from .Render import Render
from .Scene import Scene
from .Analytics import Analytics


if BlenderActions.getBlenderVersion() and BlenderActions.getBlenderVersion() < BlenderDefinitions.BlenderVersions.TWO_DOT_EIGHTY.value:
    print(
        f"CodeToCAD BlenderProvider only supports Blender versions {'.'.join(tuple, BlenderDefinitions.BlenderVersions.TWO_DOT_EIGHTY.value)}+. You are running version {'.'.join(BlenderActions.getBlenderVersion())}")  # type: ignore


def injectBlenderProvider(globalContext: Optional[dict]) -> None:
    from CodeToCAD import setPartProvider, setSketchProvider, setMaterialProvider, setLandmarkProvider, setJointProvider, setAnimationProvider, setSceneProvider, setAnalyticsProvider, setCameraProvider, setLightProvider, setRenderProvider

    setPartProvider(Part, globalContext)
    setSketchProvider(Sketch, globalContext)
    setMaterialProvider(Material, globalContext)
    setLandmarkProvider(Landmark, globalContext)
    setJointProvider(Joint, globalContext)
    setAnimationProvider(Animation, globalContext)
    setSceneProvider(Scene, globalContext)
    setAnalyticsProvider(Analytics, globalContext)
    setCameraProvider(Camera, globalContext)
    setLightProvider(Light, globalContext)
    setRenderProvider(Render, globalContext)
