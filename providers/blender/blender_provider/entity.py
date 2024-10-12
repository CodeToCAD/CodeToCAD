from codetocad.core.boundary_axis import BoundaryAxis
from codetocad.utilities.supported import supported
from codetocad.enums.support_level import SupportLevel
from codetocad.interfaces.entity_interface import EntityInterface
from codetocad.codetocad_types import *
from codetocad.interfaces.part_interface import PartInterface
from providers.blender.blender_provider.blender_actions.context import (
    apply_dependency_graph,
    select_object,
    update_view_layer,
)
from providers.blender.blender_provider.blender_actions.mesh import (
    get_bounding_box,
    remove_mesh,
)
from providers.blender.blender_provider.blender_actions.modifiers import clear_modifiers
from providers.blender.blender_provider.blender_actions.objects import (
    get_object,
    get_object_local_location,
    get_object_visibility,
    get_object_world_location,
    remove_object,
    set_object_visibility,
    update_object_data_name,
    update_object_landmark_names,
    update_object_name,
)
from providers.blender.blender_provider.blender_actions.transformations import (
    apply_object_transformations,
    rotate_object,
    translate_object,
)
from providers.blender.blender_provider.blender_definitions import (
    BlenderLength,
    BlenderRotationTypes,
    BlenderTranslationTypes,
)


class Entity(EntityInterface):

    def __init__(
        self, name: "str", description: "str| None" = None, native_instance=None
    ):
        self.name = name
        self.description = description
        self.native_instance = native_instance

    @supported(SupportLevel.SUPPORTED, notes="Checks for Objects with the same name.")
    def is_exists(self) -> bool:
        try:
            return get_object(self.name) is not None
        except:  # noqa: E722
            return False

    @supported(
        SupportLevel.SUPPORTED,
        notes="Renames an object and its underlying data with the same name.",
    )
    def rename(
        self, new_name: "str", renamelinked_entities_and_landmarks: "bool" = True
    ):
        assert Entity(new_name).is_exists() is False, f"{new_name} already exists."
        update_object_name(self.name, new_name)
        if renamelinked_entities_and_landmarks:
            update_object_data_name(new_name, new_name)
            update_object_landmark_names(new_name, self.name, new_name)
        self.name = new_name
        return self

    @supported(
        SupportLevel.SUPPORTED,
        notes="Deletes an object and its data with the same name. Meaning it will also delete a Mesh Object's underlying mesh. Does not check if the Mesh is being used by another Object.",
    )
    def delete(self, remove_children: "bool" = True):
        remove_object(self.name, remove_children)
        return self

    @supported(
        SupportLevel.SUPPORTED,
        notes="Checks if the object is visible in the 3D viewport, taking into account all visibility settings",
    )
    def is_visible(self) -> bool:
        return get_object_visibility(self.name)

    @supported(SupportLevel.SUPPORTED)
    def set_visible(self, is_visible: "bool"):
        set_object_visibility(self.name, is_visible)
        return self

    def _apply_modifiers_only(self):
        return self.apply(rotation=False, scale=False, location=False, modifiers=True)

    def _apply_rotation_and_scale_only(self):
        return self.apply(rotation=True, scale=True, location=False, modifiers=False)

    @supported(
        SupportLevel.PARTIAL,
        "Applies modifiers to Mesh based objects. Mileage may vary for other object types. For example, Blender does not allow applying modifiers on Curve objects, so apply() will only apply transformations.",
    )
    def apply(
        self,
        rotation: "bool" = True,
        scale: "bool" = True,
        location: "bool" = False,
        modifiers: "bool" = True,
    ) -> EntityInterface:
        update_view_layer()
        if modifiers and isinstance(self, PartInterface):
            # Only apply modifiers for Blender Objects that have meshes
            apply_dependency_graph(self.name)
            remove_mesh(self.name)
            update_object_data_name(self.name, self.name)
            clear_modifiers(self.name)
        if rotation or scale or location:
            apply_object_transformations(self.name, rotation, scale, location)
        return self

    @supported(SupportLevel.SUPPORTED)
    def get_native_instance(self) -> object:
        return get_object(self.name)

    @supported(SupportLevel.SUPPORTED)
    def get_location_world(self) -> "Point":
        update_view_layer()
        return get_object_world_location(self.name)

    @supported(SupportLevel.SUPPORTED)
    def get_location_local(self) -> "Point":
        update_view_layer()
        return get_object_local_location(self.name)

    @supported(
        SupportLevel.SUPPORTED,
        notes="Selects the object in the viewport using the object's name",
    )
    def select(self):
        select_object(self.name)
        return self

    @staticmethod
    def _translation_dimension_from_dimension_or_its_float_or_string_value(
        dimension_or_its_float_or_string_value: str | float | Dimension,
        boundary_axis: BoundaryAxis,
    ):
        dimension = Dimension.from_dimension_or_its_float_or_string_value(
            dimension_or_its_float_or_string_value, boundary_axis
        )
        return BlenderLength.convert_dimension_to_blender_unit(dimension)

    @supported(SupportLevel.SUPPORTED)
    def translate_xyz(
        self,
        x: "str|float|Dimension",
        y: "str|float|Dimension",
        z: "str|float|Dimension",
    ):
        boundingBox = get_bounding_box(self.name)
        assert (
            boundingBox.x and boundingBox.y and boundingBox.z
        ), "Could not get bounding box"
        xDimension = (
            Entity._translation_dimension_from_dimension_or_its_float_or_string_value(
                x, boundingBox.x
            )
        )
        yDimension = (
            Entity._translation_dimension_from_dimension_or_its_float_or_string_value(
                y, boundingBox.y
            )
        )
        zDimension = (
            Entity._translation_dimension_from_dimension_or_its_float_or_string_value(
                z, boundingBox.z
            )
        )
        translate_object(
            self.name,
            [xDimension, yDimension, zDimension],
            BlenderTranslationTypes.ABSOLUTE,
        )
        return self

    @supported(SupportLevel.SUPPORTED)
    def translate_x(self, amount: "str|float|Dimension"):
        boundingBox = get_bounding_box(self.name)
        assert boundingBox.x, "Could not get bounding box"
        dimension = (
            Entity._translation_dimension_from_dimension_or_its_float_or_string_value(
                amount, boundingBox.x
            )
        )
        translate_object(
            self.name, [dimension, None, None], BlenderTranslationTypes.ABSOLUTE
        )
        return self

    @supported(SupportLevel.SUPPORTED)
    def translate_y(self, amount: "str|float|Dimension"):
        boundingBox = get_bounding_box(self.name)
        assert boundingBox.y, "Could not get bounding box"
        dimension = (
            Entity._translation_dimension_from_dimension_or_its_float_or_string_value(
                amount, boundingBox.y
            )
        )
        translate_object(
            self.name, [None, dimension, None], BlenderTranslationTypes.ABSOLUTE
        )
        return self

    @supported(SupportLevel.SUPPORTED)
    def translate_z(self, amount: "str|float|Dimension"):
        boundingBox = get_bounding_box(self.name)
        assert boundingBox.z, "Could not get bounding box"
        dimension = (
            Entity._translation_dimension_from_dimension_or_its_float_or_string_value(
                amount, boundingBox.z
            )
        )
        translate_object(
            self.name, [None, None, dimension], BlenderTranslationTypes.ABSOLUTE
        )
        return self

    @supported(SupportLevel.SUPPORTED)
    def rotate_xyz(
        self, x: "str|float|Angle", y: "str|float|Angle", z: "str|float|Angle"
    ):
        xAngle = Angle.from_angle_or_its_float_or_string_value(x)
        yAngle = Angle.from_angle_or_its_float_or_string_value(y)
        zAngle = Angle.from_angle_or_its_float_or_string_value(z)
        rotate_object(self.name, [xAngle, yAngle, zAngle], BlenderRotationTypes.EULER)
        return self._apply_rotation_and_scale_only()

    @supported(SupportLevel.SUPPORTED)
    def rotate_x(self, rotation: "str|float|Angle"):
        angle = Angle.from_angle_or_its_float_or_string_value(rotation)
        rotate_object(self.name, [angle, None, None], BlenderRotationTypes.EULER)
        return self._apply_rotation_and_scale_only()

    @supported(SupportLevel.SUPPORTED)
    def rotate_y(self, rotation: "str|float|Angle"):
        angle = Angle.from_angle_or_its_float_or_string_value(rotation)
        rotate_object(self.name, [None, angle, None], BlenderRotationTypes.EULER)
        return self._apply_rotation_and_scale_only()

    @supported(SupportLevel.SUPPORTED)
    def rotate_z(self, rotation: "str|float|Angle"):
        angle = Angle.from_angle_or_its_float_or_string_value(rotation)
        rotate_object(self.name, [None, None, angle], BlenderRotationTypes.EULER)
        return self._apply_rotation_and_scale_only()

    @supported(SupportLevel.SUPPORTED)
    def get_bounding_box(self) -> "BoundaryBox":
        return get_bounding_box(self.name)

    @supported(SupportLevel.SUPPORTED)
    def get_dimensions(self) -> "Dimensions":
        dimensions = get_object(self.name).dimensions
        dimensions = [
            Dimension.from_string(dimension, BlenderLength.DEFAULT_BLENDER_UNIT.value)
            for dimension in dimensions
        ]
        return Dimensions(dimensions[0], dimensions[1], dimensions[2])
