from typing import TypeAlias, Union, Optional

from CodeToCAD.utilities import *

EntityInterface: TypeAlias
PartInterface: TypeAlias
MaterialInterface: TypeAlias
SketchInterface: TypeAlias
LandmarkInterface: TypeAlias
CameraInterface: TypeAlias


FloatOrItsStringValue: TypeAlias = Union[str, float]
IntOrFloat: TypeAlias = Union[int, float]
MaterialOrItsName: TypeAlias = Union[str, 'MaterialInterface']
PartOrItsName: TypeAlias = Union[str, 'PartInterface']
EntityOrItsName: TypeAlias = Union[str, 'EntityInterface']
SketchOrItsName: TypeAlias = Union[str, 'SketchInterface']
LandmarkOrItsName: TypeAlias = Union[str, 'LandmarkInterface']
AxisOrItsIndexOrItsName: TypeAlias = Union[str, int, Axis]
DimensionOrItsFloatOrStringValue: TypeAlias = Union[str, float, Dimension]
AngleOrItsFloatOrStringValue: TypeAlias = Union[str, float, Angle]
EntityOrItsNameOrLandmark: TypeAlias = Union[str,
                                             'EntityInterface', 'LandmarkInterface']
PointOrListOfFloatOrItsStringValue: TypeAlias = Union[str,
                                                      list[FloatOrItsStringValue], Point]
LengthUnitOrItsName: TypeAlias = Union[str, LengthUnit]
PresetLandmarkOrItsName: TypeAlias = Union[str, PresetLandmark]
CameraOrItsName: TypeAlias = Union[str, 'CameraInterface']
