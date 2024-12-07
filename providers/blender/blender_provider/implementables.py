import math
from typing import Optional

from codetocad.interfaces.entity_interface import EntityInterface
from codetocad.interfaces.landmark_interface import LandmarkInterface
from codetocad.codetocad_types import *

from codetocad.interfaces.landmarkable_interface import LandmarkableInterface
from codetocad.utilities import create_uuid_like_id, get_absolute_filepath
from providers.blender.blender_provider.blender_actions.collections import (
    assign_object_to_collection,
)

from providers.blender.blender_provider.blender_definitions import (
    BlenderLength,
    BlenderModifiers,
    BlenderRotationTypes,
    BlenderTranslationTypes,
)
from providers.blender.blender_provider.entity import Entity


from providers.blender.blender_provider.blender_actions.constraints import (
    apply_pivot_constraint,
)
from providers.blender.blender_provider.blender_actions.import_export import (
    export_object,
)
from providers.blender.blender_provider.blender_actions.mesh import (
    get_bounding_box,
    set_edges_mean_crease,
)
from providers.blender.blender_provider.blender_actions.modifiers import (
    apply_circular_pattern,
    apply_decimate_modifier,
    apply_linear_pattern,
    apply_mirror_modifier,
    apply_modifier,
    apply_screw_modifier,
)
from providers.blender.blender_provider.blender_actions.objects import (
    create_object,
    get_object,
    get_object_collection_name,
    make_parent,
)
from providers.blender.blender_provider.blender_actions.transformations import (
    rotate_object,
    scale_object,
    translate_object,
)
from providers.blender.blender_provider.landmark import Landmark


def export(self: "Entity", file_path: str, overwrite: bool = True, scale: float = 1.0):
    absoluteFilePath = get_absolute_filepath(file_path)

    export_object(self.get_native_instance(), absoluteFilePath, overwrite, scale)
    return self


def mirror(
    self: "Entity",
    mirror_across_entity: str | EntityInterface,
    axis: str | int | Axis,
    separate_resulting_entity: Optional[str],
):
    if separate_resulting_entity is not None:
        raise NotImplementedError("Not yet supported. COD-113")

    mirrorAcrossEntityName = mirror_across_entity
    if isinstance(mirrorAcrossEntityName, LandmarkInterface):
        mirrorAcrossEntityName = mirrorAcrossEntityName.get_landmark_entity_name()
    elif isinstance(mirrorAcrossEntityName, EntityInterface):
        mirrorAcrossEntityName = mirrorAcrossEntityName.name

    axis = Axis.from_string(axis)

    assert axis, f"Unknown axis {axis}. Please use 'x', 'y', or 'z'"

    apply_mirror_modifier(self.name, mirrorAcrossEntityName, axis)

    return self._apply_modifiers_only()


def linear_pattern(
    self: "Entity",
    instance_count: "int",
    offset: str | float | Dimension,
    direction_axis: str | int | Axis = "z",
):
    axis = Axis.from_string(direction_axis)

    assert axis, f"Unknown axis {axis}. Please use 'x', 'y', or 'z'"

    if isinstance(offset, str):
        offset = Dimension.from_string(offset)

    if isinstance(offset, Dimension):
        offset = BlenderLength.convert_dimension_to_blender_unit(offset)
        offset = offset.value

    apply_linear_pattern(self.get_native_instance(), instance_count, axis, offset)

    return self._apply_modifiers_only()


def circular_pattern(
    self: "Entity",
    instance_count: "int",
    separation_angle: str | float | Angle,
    center_entity_or_landmark: str | EntityInterface,
    normal_direction_axis: str | int | Axis = "z",
):
    center_entity_or_landmark_name = center_entity_or_landmark
    if isinstance(center_entity_or_landmark_name, LandmarkInterface):
        center_entity_or_landmark_name = (
            center_entity_or_landmark_name.get_landmark_entity_name()
        )
    elif isinstance(center_entity_or_landmark_name, EntityInterface):
        center_entity_or_landmark_name = center_entity_or_landmark_name.name

    if not isinstance(self, LandmarkableInterface):
        raise Exception("Expected a landmarkable entity.")

    pivot_landmark_name = create_uuid_like_id()

    self.create_landmark(pivot_landmark_name, 0, 0, 0)

    pivot_landmark_entity = self.get_landmark(
        pivot_landmark_name
    ).get_landmark_entity_name()

    apply_pivot_constraint(pivot_landmark_entity, center_entity_or_landmark_name)

    axis = Axis.from_string(normal_direction_axis)

    assert axis, f"Unknown axis {axis}. Please use 'x', 'y', or 'z'"

    angles: list[Optional[Angle]] = [Angle(0) for _ in range(3)]

    angle = separation_angle
    if isinstance(angle, str):
        angle = Angle.from_string(angle)
    elif isinstance(angle, (float, int)):
        angle = Angle(angle)

    angles[axis.value] = angle

    rotate_object(
        pivot_landmark_entity,
        angles,
        BlenderRotationTypes.EULER,
    )

    apply_circular_pattern(self.name, instance_count, pivot_landmark_entity)

    self._apply_modifiers_only()

    self.get_landmark(pivot_landmark_name).delete()

    return self

    boundingBox = get_bounding_box(self.name)

    assert boundingBox.z, "Could not get bounding box"

    dimension = Entity._parse_and_convert_dimension_to_blender_units(
        amount, boundingBox.z
    )

    translate_object(
        self.name,
        [None, None, dimension],
        BlenderTranslationTypes.ABSOLUTE,
    )

    return self


@staticmethod
def _scale_factor_from_dimension_or_its_float_or_string_value(
    dimension_or_its_float_or_string_value: str | float | Dimension,
    current_value_in_blender: float,
):
    value = Dimension.from_dimension_or_its_float_or_string_value(
        dimension_or_its_float_or_string_value, None
    )
    value_in_blender_default_length = BlenderLength.convert_dimension_to_blender_unit(
        value
    )
    return (value_in_blender_default_length / current_value_in_blender).value


def scale_xyz(
    self: "Entity",
    x: str | float | Dimension,
    y: str | float | Dimension,
    z: str | float | Dimension,
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

    scale_object(self.name, xScaleFactor, yScaleFactor, zScaleFactor)

    return self._apply_rotation_and_scale_only()


def scale_x(self: "Entity", scale: str | float | Dimension):
    scale_factor = _scale_factor_from_dimension_or_its_float_or_string_value(
        scale, self.get_dimensions().x.value
    )
    scale_object(self.name, scale_factor, None, None)
    return self._apply_rotation_and_scale_only()


def scale_y(self: "Entity", scale: str | float | Dimension):
    scale_factor = _scale_factor_from_dimension_or_its_float_or_string_value(
        scale, self.get_dimensions().y.value
    )
    scale_object(self.name, None, scale_factor, None)
    return self._apply_rotation_and_scale_only()


def scale_z(self: "Entity", scale: str | float | Dimension):
    scale_factor = _scale_factor_from_dimension_or_its_float_or_string_value(
        scale, self.get_dimensions().z.value
    )
    scale_object(self.name, None, None, scale_factor)
    return self._apply_rotation_and_scale_only()


def scale_x_by_factor(self: "Entity", scale_factor: float):
    scale_object(self.name, scale_factor, None, None)
    return self._apply_rotation_and_scale_only()


def scale_y_by_factor(self: "Entity", scale_factor: float):
    scale_object(self.name, None, scale_factor, None)
    return self._apply_rotation_and_scale_only()


def scale_z_by_factor(self: "Entity", scale_factor: float):
    scale_object(self.name, None, None, scale_factor)
    return self._apply_rotation_and_scale_only()


def scale_keep_aspect_ratio(
    self: "Entity",
    scale: str | float | Dimension,
    axis: str | int | Axis,
):
    scale = Dimension.from_dimension_or_its_float_or_string_value(scale, None)
    value_in_blender_default_length = BlenderLength.convert_dimension_to_blender_unit(
        scale
    )

    dimensionInAxis = self.get_dimensions()[Axis.from_string(axis).value]
    scale_factor: float = (value_in_blender_default_length / dimensionInAxis).value

    scale_object(self.name, scale_factor, scale_factor, scale_factor)
    return self._apply_rotation_and_scale_only()


def twist(
    self: "EntityInterface",
    angle: str | float | Angle,
    screw_pitch: str | float | Dimension,
    iterations: "int" = 1,
    axis: str | int | Axis = "z",
):
    axis = Axis.from_string(axis)

    angleParsed = Angle.from_string(angle)

    assert axis, f"Unknown axis {axis}. Please use 'x', 'y', or 'z'"

    screw_pitch = Dimension.from_string(screw_pitch)

    apply_screw_modifier(
        self.name,
        angleParsed.to_radians(),
        axis,
        screw_pitch=screw_pitch,
        iterations=iterations,
    )

    return self._apply_modifiers_only()


def remesh(self: "Entity", strategy: str, amount: float):
    if strategy == "decimate":
        apply_decimate_modifier(self.name, int(amount))
    else:
        if strategy == "crease":
            set_edges_mean_crease(self.name, 1.0)
        if strategy == "edgesplit":
            apply_modifier(
                self.name,
                BlenderModifiers.EDGE_SPLIT,
                name="EdgeDiv",
                split_angle=math.radians(30),
            )

        apply_modifier(
            self.name,
            BlenderModifiers.SUBSURF,
            name="Subdivision",
            levels=amount,
        )

    self._apply_modifiers_only()

    if strategy == "crease":
        set_edges_mean_crease(self.name, 0)

    return self


def create_landmark(
    self: EntityInterface,
    landmark_name: str,
    x: str | float | Dimension,
    y: str | float | Dimension,
    z: str | float | Dimension,
) -> "Landmark":
    bounding_box = get_bounding_box(self.name)
    local_positions = [
        Dimension.from_dimension_or_its_float_or_string_value(x, bounding_box.x),
        Dimension.from_dimension_or_its_float_or_string_value(y, bounding_box.y),
        Dimension.from_dimension_or_its_float_or_string_value(z, bounding_box.z),
    ]
    local_positions = BlenderLength.convert_dimensions_to_blender_unit(local_positions)

    if self.get_location_local().magnitude().value != 0:
        # If we're trying to create a landmark to an object that's not at origin, then we need to offset the landmark by the geometric center.

        local_location = self.get_location_local()

        local_positions[0] -= local_location.x
        local_positions[1] -= local_location.y
        local_positions[2] -= local_location.z

    landmark = Landmark(name=landmark_name, parent=self)
    landmark_object_name = landmark.get_landmark_entity_name()
    # Create an Empty object to represent the landmark
    # Using an Empty object allows us to parent the object to this Empty.
    # Parenting inherently transforms the landmark whenever the object is translated/rotated/scaled.
    # This might not work in other CodeToCAD implementations, but it does in Blender
    empty_object = create_object(landmark_object_name, None)
    empty_object.empty_display_size = 0
    # Assign the landmark to the parent's collection
    assign_object_to_collection(
        landmark_object_name, get_object_collection_name(self.name)
    )
    # Parent the landmark to the object
    make_parent(landmark_object_name, self.name)
    translate_object(
        landmark_object_name, local_positions, BlenderTranslationTypes.ABSOLUTE
    )
    return landmark


def get_landmark(self, landmark_name: str | PresetLandmark) -> "Landmark":
    if isinstance(landmark_name, LandmarkInterface):
        landmark_name = landmark_name.name
    preset: Optional[PresetLandmark] = None
    if isinstance(landmark_name, str):
        preset = PresetLandmark.from_string(landmark_name)
    if isinstance(landmark_name, PresetLandmark):
        preset = landmark_name
        landmark_name = preset.name
    landmark = Landmark(landmark_name, self.name)
    if preset is not None:
        # if preset does not exist, create it.
        try:
            get_object(landmark.get_landmark_entity_name())
        except:  # noqa: E722
            presetXYZ = preset.get_xyz()
            self.create_landmark(
                landmark_name, presetXYZ[0], presetXYZ[1], presetXYZ[2]
            )
            return landmark
    assert (
        get_object(landmark.get_landmark_entity_name()) is not None
    ), f"Landmark {landmark_name} does not exist for {self.name}."
    return landmark
