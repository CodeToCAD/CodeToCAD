from dataclasses import dataclass

from codetocad.core.angle import Angle
from codetocad.enums.boolean_operation import BooleanOperation
from codetocad.enums.preset_landmark import PresetLandmark
from codetocad.interfaces.landmark_interface import LandmarkInterface


@dataclass
class PartOptions:
    """
    :param merge_at: The landmark where this shape will be inserted at. default_value: PresetLandmark.bottom
    :param merge_with: The landmark where this shape will be inserted at relative to existing geometry in the Part. default_value: PresetLandmark.top
    :param rotation_x: If a rotation is not specified, the shape will snap to the normal of the merge_with face.
    :param rotation_y: If a rotation is not specified, the shape will snap to the normal of the merge_with face
    :param rotation_z: If a rotation is not specified, the shape will snap to the normal of the merge_with face
    :param boolean_operation: "Union merge by default. Available options: union, subtract, intersect. default_value: BooleanOperation.UNION
    """

    merge_at: str | LandmarkInterface | PresetLandmark = PresetLandmark.bottom
    merge_with: str | LandmarkInterface | PresetLandmark = PresetLandmark.top
    rotation_x: str | float | Angle | None = None
    rotation_y: str | float | Angle | None = None
    rotation_z: str | float | Angle | None = None
    boolean_operation: str | BooleanOperation = BooleanOperation.UNION
