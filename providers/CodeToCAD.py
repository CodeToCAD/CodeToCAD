from typing import Optional, Type
import core.CodeToCADInterface as CodeToCADInterface
import core.utilities as Utilities

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
Animation = None


def setPartProvider(provider: Type[CodeToCADInterface.Part], globalContext: Optional[dict]) -> None:
    global Part, Shape
    Part = provider
    Shape = provider
    if globalContext:
        globalContext["Part"] = provider
        globalContext["Shape"] = provider


def setSketchProvider(provider: Type[CodeToCADInterface.Sketch], globalContext: Optional[dict]) -> None:
    global Sketch, Curve
    Sketch = provider
    Curve = provider
    if globalContext:
        globalContext["Sketch"] = provider
        globalContext["Curve"] = provider


def setLandmarkProvider(provider: Type[CodeToCADInterface.Landmark], globalContext: Optional[dict]) -> None:
    global Landmark
    Landmark = provider
    if globalContext:
        globalContext["Landmark"] = provider


def setSceneProvider(provider: Type[CodeToCADInterface.Scene], globalContext: Optional[dict]) -> None:
    global Scene
    Scene = provider
    if globalContext:
        globalContext["Scene"] = provider


def setAnalyticsProvider(provider: Type[CodeToCADInterface.Analytics], globalContext: Optional[dict]) -> None:
    global Analytics
    Analytics = provider
    if globalContext:
        globalContext["Analytics"] = provider


def setJointProvider(provider: Type[CodeToCADInterface.Joint], globalContext: Optional[dict]) -> None:
    global Joint
    Joint = provider
    if globalContext:
        globalContext["Joint"] = provider


def setMaterialProvider(provider: Type[CodeToCADInterface.Material], globalContext: Optional[dict]) -> None:
    global Material
    Material = provider
    if globalContext:
        globalContext["Material"] = provider


def setAnimationProvider(provider, globalContext: Optional[dict]) -> None:
    global Animation
    Animation = provider
    if globalContext:
        globalContext["Animation"] = provider
