# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.

from abc import ABCMeta, abstractmethod


from codetocad.codetocad_types import *

from typing import Self


from codetocad.interfaces.entity_interface import EntityInterface


class AnalyticsInterface(metaclass=ABCMeta):
    """
    Tools for collecting data about the entities and scene.
    """

    @abstractmethod
    def measure_distance(
        self, entity1: "str|EntityInterface", entity2: "str|EntityInterface"
    ) -> "Dimensions":
        """
        The ubiquitous ruler.
        """

        print(
            "measure_distance is called in an abstract method. Please override this method."
        )

        raise NotImplementedError()

    @abstractmethod
    def measure_angle(
        self,
        entity1: "str|EntityInterface",
        entity2: "str|EntityInterface",
        pivot: "str|EntityInterface| None" = None,
    ) -> "list[Angle]":
        """
        The ubiquitous ruler.
        """

        print(
            "measure_angle is called in an abstract method. Please override this method."
        )

        raise NotImplementedError()

    @abstractmethod
    def get_world_pose(self, entity: "str|EntityInterface") -> "list[float]":
        """
        Returns the world pose of an entity.
        """

        print(
            "get_world_pose is called in an abstract method. Please override this method."
        )

        raise NotImplementedError()

    @abstractmethod
    def get_bounding_box(self, entity_name: "str|EntityInterface") -> "BoundaryBox":
        """
        Returns the bounding box of an entity.
        """

        print(
            "get_bounding_box is called in an abstract method. Please override this method."
        )

        raise NotImplementedError()

    @abstractmethod
    def get_dimensions(self, entity_name: "str|EntityInterface") -> "Dimensions":
        """
        Returns the dimensions of an entity.
        """

        print(
            "get_dimensions is called in an abstract method. Please override this method."
        )

        raise NotImplementedError()

    @abstractmethod
    def log(self, message: "str") -> Self:
        """
        Write a message
        """

        print("log is called in an abstract method. Please override this method.")

        raise NotImplementedError()
