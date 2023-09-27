from typing import Optional, Type
from . import utilities as Utilities

from .utilities import min, max, center, Dimension, Dimensions, PresetLandmark, Angle
from .providersSample import *
from .interfaces import *

# This is the CodeToCAD provider.
# Use the following import line in your CodeToCAD file:
# from CodeToCAD import Part, Sketch, Landmark, Scene, Analytics, Joint, Material, Animation, min, max, center, Dimension, Dimensions, PresetLandmark, Angle, Camera, Light, Render

Shape: Type[PartInterface] = Part
Curve: Type[SketchInterface] = Sketch


def setPartProvider(provider: Type[PartInterface], globalContext: Optional[dict]) -> None:
    global Part, Shape
    Part = provider
    Shape = provider
    if globalContext and "Part" in globalContext:
        globalContext["Part"] = provider
    if globalContext and "Shape" in globalContext:
        globalContext["Shape"] = provider


def setSketchProvider(provider: Type[SketchInterface], globalContext: Optional[dict]) -> None:
    global Sketch, Curve
    Sketch = provider
    Curve = provider
    if globalContext and "Sketch" in globalContext:
        globalContext["Sketch"] = provider
    if globalContext and "Curve" in globalContext:
        globalContext["Curve"] = provider


def setLandmarkProvider(provider: Type[LandmarkInterface], globalContext: Optional[dict]) -> None:
    global Landmark
    Landmark = provider
    if globalContext and "Landmark" in globalContext:
        globalContext["Landmark"] = provider


def setSceneProvider(provider: Type[SceneInterface], globalContext: Optional[dict]) -> None:
    global Scene
    Scene = provider
    if globalContext and "Scene" in globalContext:
        globalContext["Scene"] = provider


def setAnalyticsProvider(provider: Type[AnalyticsInterface], globalContext: Optional[dict]) -> None:
    global Analytics
    Analytics = provider
    if globalContext and "Analytics" in globalContext:
        globalContext["Analytics"] = provider


def setJointProvider(provider: Type[JointInterface], globalContext: Optional[dict]) -> None:
    global Joint
    Joint = provider
    if globalContext and "Joint" in globalContext:
        globalContext["Joint"] = provider


def setMaterialProvider(provider: Type[MaterialInterface], globalContext: Optional[dict]) -> None:
    global Material
    Material = provider
    if globalContext and "Material" in globalContext:
        globalContext["Material"] = provider


def setAnimationProvider(provider, globalContext: Optional[dict]) -> None:
    global Animation
    Animation = provider
    if globalContext and "Animation" in globalContext:
        globalContext["Animation"] = provider


def setCameraProvider(provider, globalContext: Optional[dict]) -> None:
    global Camera
    Camera = provider
    if globalContext and "Camera" in globalContext:
        globalContext["Camera"] = provider


def setLightProvider(provider, globalContext: Optional[dict]) -> None:
    global Light
    Light = provider
    if globalContext and "Light" in globalContext:
        globalContext["Light"] = provider


def setRenderProvider(provider, globalContext: Optional[dict]) -> None:
    global Render
    Render = provider
    if globalContext and "Render" in globalContext:
        globalContext["Render"] = provider
