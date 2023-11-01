# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.

from typing import Optional
from abc import ABCMeta, abstractmethod

from codetocad.codetocad_types import *
from codetocad.utilities import *
from codetocad.core import *
from codetocad.enums import *


from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from . import EntityInterface


class AnalyticsInterface(metaclass=ABCMeta):
    """Tools for collecting data about the entities and scene."""

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def measure_distance(
        self, entity1: EntityOrItsName, entity2: EntityOrItsName
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
        entity1: EntityOrItsName,
        entity2: EntityOrItsName,
        pivot: Optional[EntityOrItsName] = None,
    ) -> "list[Angle]":
        """
        The ubiquitous ruler.
        """

        print(
            "measure_angle is called in an abstract method. Please override this method."
        )
        raise NotImplementedError()

    @abstractmethod
    def get_world_pose(self, entity: EntityOrItsName) -> "list[float]":
        """
        Returns the world pose of an entity.
        """

        print(
            "get_world_pose is called in an abstract method. Please override this method."
        )
        raise NotImplementedError()

    @abstractmethod
    def get_bounding_box(self, entity_name: EntityOrItsName) -> "BoundaryBox":
        """
        Returns the bounding box of an entity.
        """

        print(
            "get_bounding_box is called in an abstract method. Please override this method."
        )
        raise NotImplementedError()

    @abstractmethod
    def get_dimensions(self, entity_name: EntityOrItsName) -> "Dimensions":
        """
        Returns the dimensions of an entity.
        """

        print(
            "get_dimensions is called in an abstract method. Please override this method."
        )
        raise NotImplementedError()

    @abstractmethod
    def log(self, message: str):
        """
        Write a message
        """

        print("log is called in an abstract method. Please override this method.")
        return self
