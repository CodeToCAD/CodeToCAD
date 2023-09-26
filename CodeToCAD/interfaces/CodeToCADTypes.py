from typing import TypeAlias, Union, Optional

from CodeToCAD.utilities import *

Material: TypeAlias
Part: TypeAlias
Entity: TypeAlias
Sketch: TypeAlias
Landmark: TypeAlias
Camera: TypeAlias
Scene: TypeAlias
Animation: TypeAlias

FloatOrItsStringValue: TypeAlias = Union[str, float]
IntOrFloat: TypeAlias = Union[int, float]
MaterialOrItsName: TypeAlias = Union[str, 'Material']
PartOrItsName: TypeAlias = Union[str, 'Part']
EntityOrItsName: TypeAlias = Union[str, 'Entity']
SketchOrItsName: TypeAlias = Union[str, 'Sketch']
LandmarkOrItsName: TypeAlias = Union[str, 'Landmark']
AxisOrItsIndexOrItsName: TypeAlias = Union[str, int, Axis]
DimensionOrItsFloatOrStringValue: TypeAlias = Union[str, float, Dimension]
AngleOrItsFloatOrStringValue: TypeAlias = Union[str, float, Angle]
EntityOrItsNameOrLandmark: TypeAlias = Union[str, 'Entity', 'Landmark']
PointOrListOfFloatOrItsStringValue: TypeAlias = Union[str,
                                                      list[FloatOrItsStringValue], Point]
LengthUnitOrItsName: TypeAlias = Union[str, LengthUnit]
PresetLandmarkOrItsName: TypeAlias = Union[str, PresetLandmark]
CameraOrItsName: TypeAlias = Union[str, 'Camera']
