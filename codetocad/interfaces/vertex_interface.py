# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.

from abc import ABCMeta, abstractmethod


from codetocad.codetocad_types import *

from typing import Self


from codetocad.interfaces.projectable_interface import ProjectableInterface

from codetocad.interfaces.entity_interface import EntityInterface


class VertexInterface(EntityInterface, ProjectableInterface, metaclass=ABCMeta):
    """
    A single point in space, or a control point.
    """

    @abstractmethod
    def __init__(
        self,
        name: "str",
        location: "Point",
        description: "str| None" = None,
        native_instance=None,
        parent_entity: "str|EntityInterface| None" = None,
    ):

        self.name = name
        self.location = location
        self.description = description
        self.native_instance = native_instance
        self.parent_entity = parent_entity

    @abstractmethod
    def get_control_points(
        self,
    ) -> "list[Point]":
        """
        Get a vertex's curve control points. This may not be applicable for some curve types.
        """

        print(
            "get_control_points is called in an abstract method. Please override this method."
        )

        raise NotImplementedError()

    @abstractmethod
    def set_control_points(
        self, points: "list[str|list[str]|list[float]|list[Dimension]|Point]"
    ) -> Self:
        """
        Set a vertex's curve control points. This may not be applicable for some curve types.
        """

        print(
            "set_control_points is called in an abstract method. Please override this method."
        )

        raise NotImplementedError()
