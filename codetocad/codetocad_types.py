from typing import TypeAlias, Union

from codetocad.core import Dimension, Angle, Point, Dimensions
from codetocad.enums import Axis, LengthUnit, PresetLandmark, PresetMaterial

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from codetocad.interfaces.booleanable_interface import BooleanableInterface
    from codetocad.interfaces.camera_interface import CameraInterface
    from codetocad.interfaces.entity_interface import EntityInterface
    from codetocad.interfaces.exportable_interface import ExportableInterface
    from codetocad.interfaces.landmark_interface import LandmarkInterface
    from codetocad.interfaces.landmarkable_interface import LandmarkableInterface
    from codetocad.interfaces.vertex_interface import VertexInterface
    from codetocad.interfaces.material_interface import MaterialInterface
    from codetocad.interfaces.part_interface import PartInterface
    from codetocad.interfaces.sketch_interface import SketchInterface

MaterialOrItsName: TypeAlias = Union[str, PresetMaterial, "MaterialInterface"]
PartOrItsName: TypeAlias = Union[str, "PartInterface"]
EntityOrItsName: TypeAlias = Union[str, "EntityInterface"]
SketchOrItsName: TypeAlias = Union[str, "SketchInterface"]
LandmarkOrItsName: TypeAlias = Union[str, "LandmarkInterface"]
CameraOrItsName: TypeAlias = Union[str, "CameraInterface"]
ExportableOrItsName: TypeAlias = Union[str, "ExportableInterface"]
BooleanableOrItsName: TypeAlias = Union[str, "BooleanableInterface"]
LandmarkableOrItsName: TypeAlias = Union[str, "LandmarkableInterface"]


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
