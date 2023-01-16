import core.CodeToCADInterface as CodeToCADInterface
import core.utilities as Utilities

# This is the CodeToCAD provider.
# Use the following import line in your CodeToCAD file:
# from CodeToCAD import Part, Shape, Sketch, Curve, Landmark, Scene, Analytics, Joint, Material, Animation, min, max, center, Dimension, Dimensions, Angle

min = Utilities.min
max = Utilities.max
center = Utilities.center
Dimension = Utilities.Dimension
Dimensions = Utilities.Dimensions
Angle = Utilities.Angle

Part: CodeToCADInterface.Part = None
Shape: CodeToCADInterface.Part = None
Sketch: CodeToCADInterface.Sketch = None
Curve: CodeToCADInterface.Sketch = None
Landmark: CodeToCADInterface.Landmark = None
Scene: CodeToCADInterface.Scene = None
Analytics: CodeToCADInterface.Analytics = None
Joint: CodeToCADInterface.Joint = None
Material: CodeToCADInterface.Material = None
Animation = None


def setPartProvider(provider):
    global Part, Shape
    Part = provider
    Shape = provider


def setSketchProvider(provider):
    global Sketch, Curve
    Sketch = provider
    Curve = provider


def setLandmarkProvider(provider):
    global Landmark
    Landmark = provider


def setSceneProvider(provider):
    global Scene
    Scene = provider


def setAnalyticsProvider(provider):
    global Analytics
    Analytics = provider


def setJointProvider(provider):
    global Joint
    Joint = provider


def setMaterialProvider(provider):
    global Material
    Material = provider


def setAnimationProvider(provider):
    global Animation
    Animation = provider
