from codetocad.core.boundary_axis import BoundaryAxis
from typing import Self
from codetocad.interfaces.sketch_interface import SketchInterface
from codetocad.utilities.override import override
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
from providers.blender.blender_provider.blender_actions.curve import (
    get_curve,
    get_curve_or_none,
)
from providers.blender.blender_provider.blender_actions.mesh import (
    get_bounding_box,
    get_mesh,
    remove_mesh,
)
from providers.blender.blender_provider.blender_actions.modifiers import clear_modifiers
from providers.blender.blender_provider.blender_actions.objects import (
    get_object,
    get_object_local_location,
    get_object_or_none,
    get_object_visibility,
    get_object_world_location,
    remove_data,
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
    BlenderTypes,
)


class Entity(EntityInterface):

    def __init__(self, native_instance: "Any"):
        self.native_instance = native_instance

    @override
    @property
    def name(self) -> "str":
        """
        The @overide only exists to trick the provider_update script to not remove the name property.

        Returns the name of the entity in Blender.
        """
        return self.native_instance.name

    @supported(SupportLevel.SUPPORTED, notes="")
    def is_exists(self) -> bool:
        if isinstance(self, SketchInterface):
            return get_curve_or_none(self.name) is not None
        return get_object_or_none(self.name) is not None

    @supported(SupportLevel.SUPPORTED, notes="")
    def delete(self, remove_children: "bool" = True):
        if isinstance(self, SketchInterface):
            sketch_object = get_object_or_none(self.name, BlenderTypes.CURVE.value)
            if sketch_object is None:
                curve_data = get_curve(self.name)
                remove_data(curve_data)
                return
        remove_object(self.name, remove_children)
        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def is_visible(self) -> bool:
        return get_object_visibility(self.name)

    @supported(SupportLevel.SUPPORTED, notes="")
    def set_visible(self, is_visible: "bool"):
        set_object_visibility(self.name, is_visible)
        return self

    def _apply_modifiers_only(self):
        return self.apply(rotation=False, scale=False, location=False, modifiers=True)

    def _apply_rotation_and_scale_only(self):
        return self.apply(rotation=True, scale=True, location=False, modifiers=False)

    @supported(SupportLevel.SUPPORTED, notes="")
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

    @supported(SupportLevel.SUPPORTED, notes="")
    def get_native_instance(self) -> object:
        blender_object = get_object_or_none(self.name)
        if blender_object:
            return blender_object
        if isinstance(self, SketchInterface):
            return get_curve(self.name)
        if isinstance(self, PartInterface):
            return get_mesh(self.name)
        raise NotImplementedError("get_native_instance is not supported")

    @supported(SupportLevel.SUPPORTED, notes="")
    def get_location_world(self) -> "Point":
        update_view_layer()
        return get_object_world_location(self.name)

    @supported(SupportLevel.SUPPORTED, notes="")
    def get_location_local(self) -> "Point":
        update_view_layer()
        return get_object_local_location(self.name)

    @supported(SupportLevel.SUPPORTED, notes="")
    def select(self):
        select_object(self.name)
        return self

    @staticmethod
    def _parse_and_convert_dimension_to_blender_units(
        dimension_or_its_float_or_string_value: str | float | Dimension,
        boundary_axis: BoundaryAxis | None = None,
    ):
        dimension = Dimension.from_dimension_or_its_float_or_string_value(
            dimension_or_its_float_or_string_value, boundary_axis
        )
        return BlenderLength.convert_dimension_to_blender_unit(dimension)

    def _translate_xyz(
        self,
        x: "str|float|Dimension|None",
        y: "str|float|Dimension|None",
        z: "str|float|Dimension|None",
    ):
        boundingBox = get_bounding_box(self.name)
        assert (
            boundingBox.x and boundingBox.y and boundingBox.z
        ), "Could not get bounding box"
        x_dimension = (
            Entity._parse_and_convert_dimension_to_blender_units(x, boundingBox.x)
            if x
            else None
        )
        y_dimension = (
            Entity._parse_and_convert_dimension_to_blender_units(y, boundingBox.y)
            if y
            else None
        )
        z_dimension = (
            Entity._parse_and_convert_dimension_to_blender_units(z, boundingBox.z)
            if z
            else None
        )
        translate_object(
            self.name,
            [x_dimension, y_dimension, z_dimension],
            BlenderTranslationTypes.ABSOLUTE,
        )
        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def translate_xyz(
        self,
        x: "str|float|Dimension",
        y: "str|float|Dimension",
        z: "str|float|Dimension",
    ):
        return self._translate_xyz(x, y, z)

    @supported(SupportLevel.SUPPORTED, notes="")
    def translate_x(self, amount: "str|float|Dimension"):
        return self._translate_xyz(amount, None, None)

    @supported(SupportLevel.SUPPORTED, notes="")
    def translate_y(self, amount: "str|float|Dimension"):
        return self._translate_xyz(None, amount, None)

    @supported(SupportLevel.SUPPORTED, notes="")
    def translate_z(self, amount: "str|float|Dimension"):
        return self._translate_xyz(None, None, amount)

    def _rotate_xyz(
        self,
        x: "str|float|Angle|None",
        y: "str|float|Angle|None",
        z: "str|float|Angle|None",
        use_object_name: str | None = None,
    ):
        x_angle = Angle.from_angle_or_its_float_or_string_value(x) if x else None
        y_angle = Angle.from_angle_or_its_float_or_string_value(y) if y else None
        z_angle = Angle.from_angle_or_its_float_or_string_value(z) if z else None
        rotate_object(
            use_object_name or self.name,
            [x_angle, y_angle, z_angle],
            BlenderRotationTypes.EULER,
        )
        return self._apply_rotation_and_scale_only()

    @supported(SupportLevel.SUPPORTED, notes="")
    def rotate_xyz(
        self, x: "str|float|Angle", y: "str|float|Angle", z: "str|float|Angle"
    ):
        return self._rotate_xyz(x, y, z)

    @supported(SupportLevel.SUPPORTED, notes="")
    def rotate_x(self, rotation: "str|float|Angle"):
        return self._rotate_xyz(rotation, None, None)

    @supported(SupportLevel.SUPPORTED, notes="")
    def rotate_y(self, rotation: "str|float|Angle"):
        return self._rotate_xyz(None, rotation, None)

    @supported(SupportLevel.SUPPORTED, notes="")
    def rotate_z(self, rotation: "str|float|Angle"):
        return self._rotate_xyz(None, None, rotation)

    @supported(SupportLevel.SUPPORTED, notes="")
    def get_bounding_box(self) -> "BoundaryBox":
        return get_bounding_box(self.name)

    @supported(SupportLevel.SUPPORTED, notes="")
    def get_dimensions(self) -> "Dimensions":
        dimensions = get_object(self.name).dimensions
        dimensions = [
            Dimension.from_string(dimension, BlenderLength.DEFAULT_BLENDER_UNIT.value)
            for dimension in dimensions
        ]
        return Dimensions(dimensions[0], dimensions[1], dimensions[2])

    @supported(SupportLevel.SUPPORTED, notes="")
    def set_name(
        self, new_name: "str", rename_linked_entities_and_landmarks: "bool" = True
    ) -> Self:
        assert Entity(new_name).is_exists() is False, f"{new_name} already exists."
        update_object_name(self.name, new_name)
        if rename_linked_entities_and_landmarks:
            update_object_data_name(new_name, new_name)
            update_object_landmark_names(new_name, self.name, new_name)
        self.name = new_name
        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def get_name(self) -> "str":
        print("get_name called")
        return "String"
