from typing import TypeAlias, Union

from codetocad.core import Dimension, Angle, Point, Dimensions
from codetocad.enums import Axis, LengthUnit, PresetLandmark, PresetMaterial

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
        ExportableInterface,
    )

MaterialOrItsName: TypeAlias = Union[str, PresetMaterial, "MaterialInterface"]
PartOrItsName: TypeAlias = Union[str, "PartInterface"]
EntityOrItsName: TypeAlias = Union[str, "EntityInterface"]
SketchOrItsName: TypeAlias = Union[str, "SketchInterface"]
LandmarkOrItsName: TypeAlias = Union[str, "LandmarkInterface"]
CameraOrItsName: TypeAlias = Union[str, "CameraInterface"]
ExportableOrItsName: TypeAlias = Union[str, "ExportableInterface"]


FloatOrItsStringValue: TypeAlias = Union[str, float]
IntOrFloat: TypeAlias = Union[int, float]

AxisOrItsIndexOrItsName: TypeAlias = Union[str, int, Axis]
DimensionOrItsFloatOrStringValue: TypeAlias = Union[str, float, Dimension]
AngleOrItsFloatOrStringValue: TypeAlias = Union[str, float, Angle]
DimensionsOrItsListOfFloatOrString: TypeAlias = Union[
    str, list[FloatOrItsStringValue], list[Dimension], Dimensions
]
PointOrListOfFloatOrItsStringValue: TypeAlias = Union[
    str, list[FloatOrItsStringValue], list[Dimension], Point
]
PointOrListOfFloatOrItsStringValueOrVertex: TypeAlias = Union[
    str, list[FloatOrItsStringValue], list[Dimension], Point, "VertexInterface"
]
LengthUnitOrItsName: TypeAlias = Union[str, LengthUnit]
PresetLandmarkOrItsName: TypeAlias = Union[str, PresetLandmark]
