import math
from typing import Optional, TYPE_CHECKING

from . import blender_actions
from . import blender_definitions

from codetocad.interfaces import EntityInterface, LandmarkInterface
from codetocad.codetocad_types import *
from codetocad.utilities import *
from codetocad.core import *
from codetocad.enums import *

if TYPE_CHECKING:
    from . import Entity


def export(self: "Entity", file_path: str, overwrite: bool = True, scale: float = 1.0):
    absoluteFilePath = get_absolute_filepath(file_path)

    blender_actions.export_object(self.name, absoluteFilePath, overwrite, scale)
    return self


def mirror(
    self: "Entity",
    mirror_across_entity: EntityOrItsName,
    axis: AxisOrItsIndexOrItsName,
    resulting_mirrored_entity_name: Optional[str],
):
    if resulting_mirrored_entity_name is not None:
        raise NotImplementedError("Not yet supported. COD-113")

    mirrorAcrossEntityName = mirror_across_entity
    if isinstance(mirrorAcrossEntityName, LandmarkInterface):
        mirrorAcrossEntityName = mirrorAcrossEntityName.get_landmark_entity_name()
    elif isinstance(mirrorAcrossEntityName, EntityInterface):
        mirrorAcrossEntityName = mirrorAcrossEntityName.name

    axis = Axis.from_string(axis)

    assert axis, f"Unknown axis {axis}. Please use 'x', 'y', or 'z'"

    blender_actions.apply_mirror_modifier(self.name, mirrorAcrossEntityName, axis)

    return self._apply_modifiers_only()


def linear_pattern(
    self: "Entity",
    instance_count: "int",
    offset: DimensionOrItsFloatOrStringValue,
    direction_axis: AxisOrItsIndexOrItsName = "z",
):
    axis = Axis.from_string(direction_axis)

    assert axis, f"Unknown axis {axis}. Please use 'x', 'y', or 'z'"

    if isinstance(offset, str):
        offset = Dimension.from_string(offset)

    if isinstance(offset, Dimension):
        offset = blender_definitions.BlenderLength.convert_dimension_to_blender_unit(
            offset
        )
        offset = offset.value

    blender_actions.apply_linear_pattern(self.name, instance_count, axis, offset)

    return self._apply_modifiers_only()


def circular_pattern(
    self: "Entity",
    instance_count: "int",
    separation_angle: AngleOrItsFloatOrStringValue,
    center_entity_or_landmark: EntityOrItsName,
    normal_direction_axis: AxisOrItsIndexOrItsName = "z",
):
    center_entity_or_landmark_name = center_entity_or_landmark
    if isinstance(center_entity_or_landmark_name, LandmarkInterface):
        center_entity_or_landmark_name = (
            center_entity_or_landmark_name.get_landmark_entity_name()
        )
    elif isinstance(center_entity_or_landmark_name, EntityInterface):
        center_entity_or_landmark_name = center_entity_or_landmark_name.name

    pivotLandmarkName = create_uuid_like_id()

    self.create_landmark(pivotLandmarkName, 0, 0, 0)

    pivotLandmarkEntityName = self.get_landmark(
        pivotLandmarkName
    ).get_landmark_entity_name()

    blender_actions.apply_pivot_constraint(
        pivotLandmarkEntityName, center_entity_or_landmark_name
    )

    axis = Axis.from_string(normal_direction_axis)

    assert axis, f"Unknown axis {axis}. Please use 'x', 'y', or 'z'"

    angles: list[Optional[Angle]] = [Angle(0) for _ in range(3)]

    angle = separation_angle
    if isinstance(angle, str):
        angle = Angle.from_string(angle)
    elif isinstance(angle, (float, int)):
        angle = Angle(angle)

    angles[axis.value] = angle

    blender_actions.rotate_object(
        pivotLandmarkEntityName,
        angles,
        blender_definitions.BlenderRotationTypes.EULER,
    )

    blender_actions.apply_circular_pattern(
        self.name, instance_count, pivotLandmarkEntityName
    )

    self._apply_modifiers_only()

    self.get_landmark(pivotLandmarkName).delete()

    return self

    boundingBox = blender_actions.get_bounding_box(self.name)

    assert boundingBox.z, "Could not get bounding box"

    dimension = (
        Entity._translation_dimension_from_dimension_or_its_float_or_string_value(
            amount, boundingBox.z
        )
    )

    blender_actions.translate_object(
        self.name,
        [None, None, dimension],
        blender_definitions.BlenderTranslationTypes.ABSOLUTE,
    )

    return self


@staticmethod
def _scale_factor_from_dimension_or_its_float_or_string_value(
    dimension_or_its_float_or_string_value: DimensionOrItsFloatOrStringValue,
    current_value_in_blender: float,
):
    value = Dimension.from_dimension_or_its_float_or_string_value(
        dimension_or_its_float_or_string_value, None
    )
    valueInBlenderDefaultLength = (
        blender_definitions.BlenderLength.convert_dimension_to_blender_unit(value)
    )
    return (valueInBlenderDefaultLength / current_value_in_blender).value


def scale_xyz(
    self: "Entity",
    x: DimensionOrItsFloatOrStringValue,
    y: DimensionOrItsFloatOrStringValue,
    z: DimensionOrItsFloatOrStringValue,
):
    currentDimensions = self.get_dimensions()
    xScaleFactor: float = _scale_factor_from_dimension_or_its_float_or_string_value(
        x, currentDimensions.x.value
    )
    yScaleFactor: float = _scale_factor_from_dimension_or_its_float_or_string_value(
        y, currentDimensions.y.value
    )
    zScaleFactor: float = _scale_factor_from_dimension_or_its_float_or_string_value(
        z, currentDimensions.z.value
    )

    blender_actions.scale_object(self.name, xScaleFactor, yScaleFactor, zScaleFactor)

    return self._apply_rotation_and_scale_only()


def scale_x(self: "Entity", scale: DimensionOrItsFloatOrStringValue):
    scale_factor = _scale_factor_from_dimension_or_its_float_or_string_value(
        scale, self.get_dimensions().x.value
    )
    blender_actions.scale_object(self.name, scale_factor, None, None)
    return self._apply_rotation_and_scale_only()


def scale_y(self: "Entity", scale: DimensionOrItsFloatOrStringValue):
    scale_factor = _scale_factor_from_dimension_or_its_float_or_string_value(
        scale, self.get_dimensions().y.value
    )
    blender_actions.scale_object(self.name, None, scale_factor, None)
    return self._apply_rotation_and_scale_only()


def scale_z(self: "Entity", scale: DimensionOrItsFloatOrStringValue):
    scale_factor = _scale_factor_from_dimension_or_its_float_or_string_value(
        scale, self.get_dimensions().z.value
    )
    blender_actions.scale_object(self.name, None, None, scale_factor)
    return self._apply_rotation_and_scale_only()


def scale_x_by_factor(self: "Entity", scale_factor: float):
    blender_actions.scale_object(self.name, scale_factor, None, None)
    return self._apply_rotation_and_scale_only()


def scale_y_by_factor(self: "Entity", scale_factor: float):
    blender_actions.scale_object(self.name, None, scale_factor, None)
    return self._apply_rotation_and_scale_only()


def scale_z_by_factor(self: "Entity", scale_factor: float):
    blender_actions.scale_object(self.name, None, None, scale_factor)
    return self._apply_rotation_and_scale_only()


def scale_keep_aspect_ratio(
    self: "Entity",
    scale: DimensionOrItsFloatOrStringValue,
    axis: AxisOrItsIndexOrItsName,
):
    scale = Dimension.from_dimension_or_its_float_or_string_value(scale, None)
    valueInBlenderDefaultLength = (
        blender_definitions.BlenderLength.convert_dimension_to_blender_unit(scale)
    )

    dimensionInAxis = self.get_dimensions()[Axis.from_string(axis).value]
    scale_factor: float = (valueInBlenderDefaultLength / dimensionInAxis).value

    blender_actions.scale_object(self.name, scale_factor, scale_factor, scale_factor)
    return self._apply_rotation_and_scale_only()


def twist(
    self: "Entity",
    angle: AngleOrItsFloatOrStringValue,
    screw_pitch: DimensionOrItsFloatOrStringValue,
    iterations: "int" = 1,
    axis: AxisOrItsIndexOrItsName = "z",
):
    axis = Axis.from_string(axis)

    angleParsed = Angle.from_string(angle)

    assert axis, f"Unknown axis {axis}. Please use 'x', 'y', or 'z'"

    screw_pitch = Dimension.from_string(screw_pitch)

    blender_actions.apply_screw_modifier(
        self.name,
        angleParsed.to_radians(),
        axis,
        screw_pitch=screw_pitch,
        iterations=iterations,
    )

    return self._apply_modifiers_only()


def remesh(self: "Entity", strategy: str, amount: float):
    if strategy == "decimate":
        blender_actions.apply_decimate_modifier(self.name, int(amount))
    else:
        if strategy == "crease":
            blender_actions.set_edges_mean_crease(self.name, 1.0)
        if strategy == "edgesplit":
            blender_actions.apply_modifier(
                self.name,
                blender_definitions.BlenderModifiers.EDGE_SPLIT,
                name="EdgeDiv",
                split_angle=math.radians(30),
            )

        blender_actions.apply_modifier(
            self.name,
            blender_definitions.BlenderModifiers.SUBSURF,
            name="Subdivision",
            levels=amount,
        )

    self._apply_modifiers_only()

    if strategy == "crease":
        blender_actions.set_edges_mean_crease(self.name, 0)

    return self
