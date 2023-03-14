from typing import Optional, Type
from . import CodeToCADInterface as CodeToCADInterface
from . import utilities as Utilities

# This is the CodeToCAD provider.
# Use the following import line in your CodeToCAD file:
# from CodeToCAD import Part, Shape, Sketch, Curve, Landmark, Scene, Analytics, Joint, Material, Animation, min, max, center, Dimension, Dimensions, Angle

min: str = Utilities.min
max: str = Utilities.max
center: str = Utilities.center
Dimension: Type[Utilities.Dimension] = Utilities.Dimension
Dimensions: Type[Utilities.Dimensions] = Utilities.Dimensions
Angle: Type[Utilities.Angle] = Utilities.Angle

Part: Type[CodeToCADInterface.Part] = CodeToCADInterface.Part
Shape: Type[CodeToCADInterface.Part] = CodeToCADInterface.Part
Sketch: Type[CodeToCADInterface.Sketch] = CodeToCADInterface.Sketch
Curve: Type[CodeToCADInterface.Sketch] = CodeToCADInterface.Sketch
Landmark: Type[CodeToCADInterface.Landmark] = CodeToCADInterface.Landmark
Scene: Type[CodeToCADInterface.Scene] = CodeToCADInterface.Scene
Analytics: Type[CodeToCADInterface.Analytics] = CodeToCADInterface.Analytics
Joint: Type[CodeToCADInterface.Joint] = CodeToCADInterface.Joint
Material: Type[CodeToCADInterface.Material] = CodeToCADInterface.Material
Animation: Type[CodeToCADInterface.Animation] = CodeToCADInterface.Animation
Camera: Type[CodeToCADInterface.Camera] = CodeToCADInterface.Camera
Light: Type[CodeToCADInterface.Light] = CodeToCADInterface.Light


def setPartProvider(provider: Type[CodeToCADInterface.Part], globalContext: Optional[dict]) -> None:
    global Part, Shape
    Part = provider
    Shape = provider
    if globalContext and "Part" in globalContext:
        globalContext["Part"] = provider
    if globalContext and "Shape" in globalContext:
        globalContext["Shape"] = provider


def setSketchProvider(provider: Type[CodeToCADInterface.Sketch], globalContext: Optional[dict]) -> None:
    global Sketch, Curve
    Sketch = provider
    Curve = provider
    if globalContext and "Sketch" in globalContext:
        globalContext["Sketch"] = provider
    if globalContext and "Curve" in globalContext:
        globalContext["Curve"] = provider


def setLandmarkProvider(provider: Type[CodeToCADInterface.Landmark], globalContext: Optional[dict]) -> None:
    global Landmark
    Landmark = provider
    if globalContext and "Landmark" in globalContext:
        globalContext["Landmark"] = provider


def setSceneProvider(provider: Type[CodeToCADInterface.Scene], globalContext: Optional[dict]) -> None:
    global Scene
    Scene = provider
    if globalContext and "Scene" in globalContext:
        globalContext["Scene"] = provider


def setAnalyticsProvider(provider: Type[CodeToCADInterface.Analytics], globalContext: Optional[dict]) -> None:
    global Analytics
    Analytics = provider
    if globalContext and "Analytics" in globalContext:
        globalContext["Analytics"] = provider


def setJointProvider(provider: Type[CodeToCADInterface.Joint], globalContext: Optional[dict]) -> None:
    global Joint
    Joint = provider
    if globalContext and "Joint" in globalContext:
        globalContext["Joint"] = provider


def setMaterialProvider(provider: Type[CodeToCADInterface.Material], globalContext: Optional[dict]) -> None:
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
