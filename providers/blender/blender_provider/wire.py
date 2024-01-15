from typing import Optional

from codetocad.interfaces import WireInterface
from codetocad.codetocad_types import *
from codetocad.interfaces.projectable_interface import ProjectableInterface
from codetocad.utilities import *
from codetocad.core import *
from codetocad.enums import *


from . import Entity

from typing import TYPE_CHECKING

from . import blender_actions
from . import blender_definitions

if TYPE_CHECKING:
    from . import Edge
    from . import Vertex
    from . import Part


class Wire(Entity, WireInterface):
    edges: "list[Edge]"
    parent_entity: Optional[EntityOrItsName] = None
    name: str
    description: Optional[str] = None
    native_instance = None

    def get_native_instance(self) -> object:
        return self.native_instance

    def __init__(
        self,
        edges: "list[Edge]",
        name: str,
        parent_entity: Optional[EntityOrItsName] = None,
        description: Optional[str] = None,
        native_instance=None,
    ):
        """
        NOTE: Blender Provider's Wire requires a parent_entity and a native_instance
        """
        assert (
            parent_entity is not None and native_instance is not None
        ), "Blender Provider's Wire requires a parent_entity and a native_instance"

        self.edges = edges
        self.parent_entity = parent_entity
        self.name = name
        self.description = description
        self.native_instance = native_instance

    def get_vertices(self) -> list["Vertex"]:
        if len(self.edges) == 0:
            return []

        all_vertices = [self.edges[0].v1, self.edges[0].v2]
        for edge in self.edges[1:]:
            all_vertices.append(edge.v2)

        return all_vertices

    def get_is_closed(self) -> bool:
        if not self.native_instance:
            raise Exception(
                "Cannot find native wire instance, this may mean that this reference is stale or the object does not exist in Blender."
            )
        return blender_actions.is_spline_cyclical(self.native_instance)

    def mirror(
        self,
        mirror_across_entity: EntityOrItsName,
        axis: AxisOrItsIndexOrItsName,
        resulting_mirrored_entity_name: Optional[str] = None,
    ):
        raise NotImplementedError()
        return self

    def project(self, project_onto: "SketchInterface") -> "ProjectableInterface":
        raise NotImplementedError()
        return self

    def linear_pattern(
        self,
        instance_count: "int",
        offset: DimensionOrItsFloatOrStringValue,
        direction_axis: AxisOrItsIndexOrItsName = "z",
    ):
        raise NotImplementedError()
        return self

    def circular_pattern(
        self,
        instance_count: "int",
        separation_angle: AngleOrItsFloatOrStringValue,
        center_entity_or_landmark: EntityOrItsName,
        normal_direction_axis: AxisOrItsIndexOrItsName = "z",
    ):
        raise NotImplementedError()
        return self

    def loft(self, other: "Wire", new_part_name: Optional[str] = None) -> "Part":
        blender_mesh = blender_actions.loft(self, other)

        from . import Part

        part = Part(blender_mesh.name)

        if new_part_name:
            part.rename(new_part_name)
        else:
            if self.parent_entity:
                parent_name = (
                    self.parent_entity.name
                    if not isinstance(self.parent_entity, str)
                    else self.parent_entity
                )

                if (
                    type(blender_actions.get_object(parent_name))
                    == blender_definitions.BlenderTypes.MESH.value
                ):
                    part.union(
                        parent_name, delete_after_union=True, is_transfer_landmarks=True
                    )
                else:
                    Entity(parent_name).delete()

                part.rename(parent_name)
            if other.parent_entity:
                parent_name = (
                    other.parent_entity.name
                    if not isinstance(other.parent_entity, str)
                    else other.parent_entity
                )

                if (
                    type(blender_actions.get_object(parent_name))
                    == blender_definitions.BlenderTypes.MESH.value
                ):
                    part.union(
                        parent_name, delete_after_union=True, is_transfer_landmarks=True
                    )
                else:
                    Entity(parent_name).delete()

        return part
