from typing import Optional
from providers.blender.blender_provider.blender_actions.context import (
    select_object,
    update_view_layer,
)

from providers.blender.blender_provider.blender_actions.objects import (
    get_object,
    get_object_local_location,
    get_object_visibility,
    get_object_world_location,
    remove_object,
    set_object_visibility,
    update_object_name,
)


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
            return get_object(self.get_landmark_entity_name()) is not None
        except:  # noqa E722
            return False

    def rename(self, new_name: str):
        assert (
            Landmark(new_name, self.parent_entity).is_exists() is False
        ), f"{new_name} already exists."

        parent_entityName = self.parent_entity
        if isinstance(parent_entityName, EntityInterface):
            parent_entityName = parent_entityName.name

        update_object_name(
            self.get_landmark_entity_name(),
            format_landmark_entity_name(parent_entityName, new_name),
        )

        self.name = new_name

        return self

    def delete(self):
        remove_object(self.get_landmark_entity_name())
        return self

    def is_visible(self) -> bool:
        return get_object_visibility(self.get_landmark_entity_name())

    def set_visible(self, is_visible: bool):
        set_object_visibility(self.get_landmark_entity_name(), is_visible)

        return self

    def get_native_instance(self):
        return get_object(self.get_landmark_entity_name())

    def get_location_world(self) -> "Point":
        update_view_layer()
        return get_object_world_location(self.get_landmark_entity_name())

    def get_location_local(self) -> "Point":
        update_view_layer()
        return get_object_local_location(self.get_landmark_entity_name())

    def select(self):
        select_object(self.get_landmark_entity_name())
        return self

    def clone(
        self,
        new_name: str,
        offset: Optional[list[Dimension]] = None,
        new_parent: Optional[Entity] = None,
    ) -> "Landmark":
        x = (
            self.get_location_local().x
            - self.get_parent_entity().get_location_local().x
        )
        y = (
            self.get_location_local().y
            - self.get_parent_entity().get_location_local().y
        )
        z = (
            self.get_location_local().z
            - self.get_parent_entity().get_location_local().z
        )

        if offset:
            offset_x, offset_y, offset_z = offset
            x += offset_x
            y += offset_y
            z += offset_z

        if new_parent:
            landmark = new_parent.create_landmark(new_name, x, y, z)
        else:
            landmark = self.get_parent_entity().create_landmark(new_name, x, y, z)

        return landmark
