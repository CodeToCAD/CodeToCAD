# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.

from abc import ABCMeta, abstractmethod


from codetocad.codetocad_types import *

from typing import Self


from codetocad.interfaces.entity_interface import EntityInterface

from codetocad.interfaces.exportable_interface import ExportableInterface


class SceneInterface(metaclass=ABCMeta):
    """
    Scene, camera, lighting, rendering, animation, simulation and GUI related functionality.
    """

    @abstractmethod
    def __init__(self, name: "str| None" = None, description: "str| None" = None):

        self.name = name
        self.description = description

    @staticmethod
    def default() -> "SceneInterface":
        """
        Get a Scene instance for the current scene.
        """

        print("default is called in an abstract method. Please override this method.")

        raise NotImplementedError()

    @abstractmethod
    def create(
        self,
    ) -> Self:
        """
        Creates a new scene.
        """

        print("create is called in an abstract method. Please override this method.")

        raise NotImplementedError()

    @abstractmethod
    def delete(
        self,
    ) -> Self:
        """
        Deletes a scene.
        """

        print("delete is called in an abstract method. Please override this method.")

        raise NotImplementedError()

    @abstractmethod
    def is_exists(
        self,
    ) -> "bool":
        """
        Check if the scene exists
        """

        print("is_exists is called in an abstract method. Please override this method.")

        raise NotImplementedError()

    @abstractmethod
    def get_selected_entity(
        self,
    ) -> "EntityInterface":
        """
        Get the selected entity in the Scene.
        """

        print(
            "get_selected_entity is called in an abstract method. Please override this method."
        )

        raise NotImplementedError()

    @abstractmethod
    def export(
        self,
        file_path: "str",
        entities: "list[str|ExportableInterface]",
        overwrite: "bool" = True,
        scale: "float" = 1.0,
    ) -> Self:
        """
        Export the entire scene or specific entities.
        """

        print("export is called in an abstract method. Please override this method.")

        raise NotImplementedError()

    @abstractmethod
    def set_default_unit(self, unit: "str|LengthUnit") -> Self:
        """
        Set the document's default measurements system.
        """

        print(
            "set_default_unit is called in an abstract method. Please override this method."
        )

        raise NotImplementedError()

    @abstractmethod
    def create_group(self, name: "str") -> Self:
        """
        Create a new group
        """

        print(
            "create_group is called in an abstract method. Please override this method."
        )

        raise NotImplementedError()

    @abstractmethod
    def delete_group(self, name: "str", remove_children: "bool") -> Self:
        """
        Delete a new group
        """

        print(
            "delete_group is called in an abstract method. Please override this method."
        )

        raise NotImplementedError()

    @abstractmethod
    def remove_from_group(self, entity_name: "str", group_name: "str") -> Self:
        """
        Removes an existing entity from a group
        """

        print(
            "remove_from_group is called in an abstract method. Please override this method."
        )

        raise NotImplementedError()

    @abstractmethod
    def assign_to_group(
        self,
        entities: "list[str|EntityInterface]",
        group_name: "str",
        remove_from_other_groups: "bool| None" = True,
    ) -> Self:
        """
        Assigns an existing entity to a new group
        """

        print(
            "assign_to_group is called in an abstract method. Please override this method."
        )

        raise NotImplementedError()

    @abstractmethod
    def set_visible(
        self, entities: "list[str|EntityInterface]", is_visible: "bool"
    ) -> Self:
        """
        Change the visibiltiy of the entity.
        """

        print(
            "set_visible is called in an abstract method. Please override this method."
        )

        raise NotImplementedError()

    @abstractmethod
    def set_background_image(
        self,
        file_path: "str",
        location_x: "str|float|Dimension| None" = 0,
        location_y: "str|float|Dimension| None" = 0,
    ) -> Self:
        """
        Set the scene background image. This can be an image or an HDRI texture.
        """

        print(
            "set_background_image is called in an abstract method. Please override this method."
        )

        raise NotImplementedError()
