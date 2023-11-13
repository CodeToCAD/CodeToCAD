from typing import TypeAlias, Union

from codetocad.core import Dimension, Angle, Point
from codetocad.enums import Axis, LengthUnit, PresetLandmark

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from codetocad.interfaces import (
        MaterialInterface,
        PartInterface,
        EntityInterface,
        SketchInterface,
        LandmarkInterface,
        CameraInterface,
        VertexInterface,
    )

MaterialOrItsName: TypeAlias = Union[str, "MaterialInterface"]
PartOrItsName: TypeAlias = Union[str, "PartInterface"]
EntityOrItsName: TypeAlias = Union[str, "EntityInterface"]
SketchOrItsName: TypeAlias = Union[str, "SketchInterface"]
LandmarkOrItsName: TypeAlias = Union[str, "LandmarkInterface"]
CameraOrItsName: TypeAlias = Union[str, "CameraInterface"]


FloatOrItsStringValue: TypeAlias = Union[str, float]
IntOrFloat: TypeAlias = Union[int, float]

AxisOrItsIndexOrItsName: TypeAlias = Union[str, int, Axis]
DimensionOrItsFloatOrStringValue: TypeAlias = Union[str, float, Dimension]
AngleOrItsFloatOrStringValue: TypeAlias = Union[str, float, Angle]
PointOrListOfFloatOrItsStringValue: TypeAlias = Union[
    str, list[FloatOrItsStringValue], Point
]
PointOrListOfFloatOrItsStringValueOrVertex: TypeAlias = Union[
    str, list[FloatOrItsStringValue], Point, "VertexInterface"
]
LengthUnitOrItsName: TypeAlias = Union[str, LengthUnit]
PresetLandmarkOrItsName: TypeAlias = Union[str, PresetLandmark]
