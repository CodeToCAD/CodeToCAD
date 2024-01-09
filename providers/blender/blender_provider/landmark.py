from typing import Optional

from . import blender_actions

from codetocad.interfaces import LandmarkInterface, EntityInterface
from codetocad.codetocad_types import *
from codetocad.utilities import *
from codetocad.core import *
from codetocad.enums import *


from . import Entity


class Landmark(Entity, LandmarkInterface):
    name: str
    parent_entity: EntityOrItsName
    description: Optional[str] = None
    native_instance = None

    def __init__(
        self,
        name: str,
        parent_entity: EntityOrItsName,
        description: Optional[str] = None,
        native_instance=None,
    ):
        self.name = name
        self.parent_entity = parent_entity
        self.description = description
        self.native_instance = native_instance

    def get_landmark_entity_name(self) -> str:
        parent_entityName = self.parent_entity

        if isinstance(parent_entityName, EntityInterface):
            parent_entityName = parent_entityName.name

        entityName = format_landmark_entity_name(parent_entityName, self.name)

        return entityName

    def get_parent_entity(self) -> "EntityInterface":
        if isinstance(self.parent_entity, str):
            return Entity(self.parent_entity)

        return self.parent_entity

    def is_exists(self) -> bool:
        try:
            return (
                blender_actions.get_object(self.get_landmark_entity_name()) is not None
            )
        except:  # noqa E722
            return False

    def rename(self, new_name: str):
        assert (
            Landmark(new_name, self.parent_entity).is_exists() is False
        ), f"{new_name} already exists."

        parent_entityName = self.parent_entity
        if isinstance(parent_entityName, EntityInterface):
            parent_entityName = parent_entityName.name

        blender_actions.update_object_name(
            self.get_landmark_entity_name(),
            format_landmark_entity_name(parent_entityName, new_name),
        )

        self.name = new_name

        return self

    def delete(self):
        blender_actions.remove_object(self.get_landmark_entity_name())
        return self

    def is_visible(self) -> bool:
        return blender_actions.get_object_visibility(self.get_landmark_entity_name())

    def set_visible(self, is_visible: bool):
        blender_actions.set_object_visibility(
            self.get_landmark_entity_name(), is_visible
        )

        return self

    def get_native_instance(self):
        return blender_actions.get_object(self.get_landmark_entity_name())

    def get_location_world(self) -> "Point":
        blender_actions.update_view_layer()
        return blender_actions.get_object_world_location(
            self.get_landmark_entity_name()
        )

    def get_location_local(self) -> "Point":
        blender_actions.update_view_layer()
        return blender_actions.get_object_local_location(
            self.get_landmark_entity_name()
        )

    def select(self):
        blender_actions.select_object(self.get_landmark_entity_name())
        return self

    def clone(
        self,
        landmark_name: str,
        offset: Optional[list[Dimension]]=None,
        parent: Optional[Entity]=None,
    ) -> "Landmark":
        x = self.get_location_local().x - self.get_parent_entity().get_location_local().x
        y = self.get_location_local().y - self.get_parent_entity().get_location_local().y
        z = self.get_location_local().z - self.get_parent_entity().get_location_local().z

        if offset:
            offset_x, offset_y, offset_z = offset
            x += offset_x
            y += offset_y
            z += offset_z

        if parent:
            landmark = parent.create_landmark(landmark_name, x, y, z)
        else:
            landmark = self.get_parent_entity().create_landmark(landmark_name, x, y, z)

        return landmark
