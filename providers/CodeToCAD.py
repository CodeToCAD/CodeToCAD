from typing import Type
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


def setPartProvider(provider: Type[CodeToCADInterface.Part]) -> None:
    global Part, Shape
    Part = provider
    Shape = provider


def setSketchProvider(provider: Type[CodeToCADInterface.Sketch]) -> None:
    global Sketch, Curve
    Sketch = provider
    Curve = provider


def setLandmarkProvider(provider: Type[CodeToCADInterface.Landmark]) -> None:
    global Landmark
    Landmark = provider


def setSceneProvider(provider: Type[CodeToCADInterface.Scene]) -> None:
    global Scene
    Scene = provider


def setAnalyticsProvider(provider: Type[CodeToCADInterface.Analytics]) -> None:
    global Analytics
    Analytics = provider


def setJointProvider(provider: Type[CodeToCADInterface.Joint]) -> None:
    global Joint
    Joint = provider


def setMaterialProvider(provider: Type[CodeToCADInterface.Material]) -> None:
    global Material
    Material = provider


def setAnimationProvider(provider) -> None:
    global Animation
    Animation = provider
