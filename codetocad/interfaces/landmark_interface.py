# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.

from abc import ABCMeta, abstractmethod


from codetocad.codetocad_types import *
from codetocad.utilities import *
from codetocad.core import *
from codetocad.enums import *


from codetocad.interfaces.entity_interface import EntityInterface


class LandmarkInterface(metaclass=ABCMeta):

    """
    Landmarks are named positions on an entity.
    """

    @abstractmethod
    def __init__(
        self,
        name: "str",
        parent_entity: "EntityOrItsName",
        description: "str| None" = None,
    ):
        self.name = name
        self.parent_entity = parent_entity
        self.description = description

    @abstractmethod
    def get_location_world(
        self,
    ) -> "Point":
        """
        Get the Landmark XYZ location relative to World Space.
        """

        print(
            "get_location_world is called in an abstract method. Please override this method."
        )

        raise NotImplementedError()

    @abstractmethod
    def get_location_local(
        self,
    ) -> "Point":
        """
        Get the Landmark XYZ location relative to Local Space.
        """

        print(
            "get_location_local is called in an abstract method. Please override this method."
        )

        raise NotImplementedError()

    @abstractmethod
    def translate_xyz(
        self,
        x: "DimensionOrItsFloatOrStringValue",
        y: "DimensionOrItsFloatOrStringValue",
        z: "DimensionOrItsFloatOrStringValue",
    ):
        """
        Translate in the XYZ directions. Pass a number, Dimension or Dimension-String (e.g. '2cm') to scale to a specific length.
        """

        print(
            "translate_xyz is called in an abstract method. Please override this method."
        )

        raise NotImplementedError()

    @abstractmethod
    def clone(
        self,
        new_name: "str",
        offset: "DimensionsOrItsListOfFloatOrString| None" = None,
        new_parent: "EntityOrItsName| None" = None,
    ) -> "LandmarkInterface":
        """
        Clone an existing Landmark with an optional offset, and reassignment to a different parent. Returns the new Landmark.
        """

        print("clone is called in an abstract method. Please override this method.")

        raise NotImplementedError()

    @abstractmethod
    def get_landmark_entity_name(
        self,
    ) -> "str":
        """
        Get the landmark object name in the scene, which may be different to the name of the landmark when it was first created. For example, the generated name may be {parentName}_{landmarkName}.
        """

        print(
            "get_landmark_entity_name is called in an abstract method. Please override this method."
        )

        raise NotImplementedError()

    @abstractmethod
    def get_parent_entity(
        self,
    ) -> "EntityInterface":
        """
        Get the name of the entity this landmark belongs to.
        """

        print(
            "get_parent_entity is called in an abstract method. Please override this method."
        )

        raise NotImplementedError()
