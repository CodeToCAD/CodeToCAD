# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.

from abc import ABCMeta, abstractmethod


from codetocad.codetocad_types import *


from codetocad.interfaces.entity_interface import EntityInterface


class LandmarkInterface(EntityInterface, metaclass=ABCMeta):
    """
    Landmarks are named positions on an entity.
    """

    @abstractmethod
    def __init__(
        self,
        name: "str",
        parent_entity: "str|EntityInterface",
        description: "str| None" = None,
        native_instance=None,
    ):

        self.name = name
        self.parent_entity = parent_entity
        self.description = description
        self.native_instance = native_instance

    @abstractmethod
    def clone(
        self,
        new_name: "str",
        offset: "str|list[str]|list[float]|list[Dimension]|Dimensions| None" = None,
        new_parent: "str|EntityInterface| None" = None,
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
