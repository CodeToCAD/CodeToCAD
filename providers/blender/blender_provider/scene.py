from typing import Optional

from . import blender_actions
from . import blender_definitions

from codetocad.interfaces import SceneInterface, EntityInterface
from codetocad.codetocad_types import *
from codetocad.utilities import *

from .part import Part
from .entity import Entity


class Scene(SceneInterface):

    # Blender's default Scene name is "Scene"
    name: str = "Scene"
    description: Optional[str] = None

    def __init__(self, name: Optional[str] = None, description: Optional[str] = None):
        self.name = name or self.name
        self.description = description

    @staticmethod
    def default(
    ) -> 'Scene':
        return Scene()

    def create(self
               ):
        raise NotImplementedError()
        return self

    def delete(self
               ):
        raise NotImplementedError()
        return self

    def get_selected_entity(self) -> 'EntityInterface':

        return Entity(blender_actions.get_selected_object_name())

    def export(self, file_path: str, entities: list[EntityOrItsName], overwrite: bool = True, scale: float = 1.0
               ):
        for entity in entities:
            part = entity
            if isinstance(part, str):
                part = Part(part)
            part.export(file_path, overwrite, scale)
        return self

    def set_default_unit(self, unit: LengthUnitOrItsName
                         ):
        if isinstance(unit, str):
            unit = LengthUnit.from_string(unit)

        blenderUnit = blender_definitions.BlenderLength.from_length_unit(unit)

        blender_actions.set_default_unit(blenderUnit, self.name)
        return self

    def create_group(self, name: str
                     ):
        blender_actions.create_collection(name, self.name)
        return self

    def delete_group(self, name: str, remove_children: bool
                     ):
        blender_actions.remove_collection(
            name=name,
            scene_name=self.name,
            remove_children=remove_children
        )
        return self

    def remove_from_group(self, entity_name: str, group_name: str
                          ):
        if isinstance(entity_name, Entity):
            entity_name = entity_name.name

        blender_actions.remove_object_from_collection(
            existing_object_name=entity_name,
            collection_name=group_name,
            scene_name=self.name
        )
        return self

    def assign_to_group(self, entities: list[EntityOrItsName], group_name: str, remove_from_other_groups: Optional[bool] = True
                        ):
        for entity in entities:
            entity_name = entity
            if isinstance(entity_name, EntityInterface):
                entity_name = entity_name.name

            blender_actions.assign_object_to_collection(
                entity_name, group_name, self.name, remove_from_other_groups or True)

        return self

    def set_visible(self, entities: list[EntityOrItsName], is_visible: bool
                    ):

        for entity in entities:
            if isinstance(entity, EntityInterface):
                entity = entity.name

            blender_actions.set_object_visibility(entity, is_visible)

        return self

    def set_background_image(self, file_path: str, location_x: Optional[DimensionOrItsFloatOrStringValue] = 0, location_y: Optional[DimensionOrItsFloatOrStringValue] = 0):

        absoluteFilePath = get_absolute_filepath(file_path)

        blender_actions.add_hdr_texture(self.name, absoluteFilePath)

        x = blender_definitions.BlenderLength.convert_dimension_to_blender_unit(
            Dimension.from_string(location_x or 0)).value
        y = blender_definitions.BlenderLength.convert_dimension_to_blender_unit(
            Dimension.from_string(location_y or 0)).value

        blender_actions.set_background_location(self.name, x, y)

        return self
