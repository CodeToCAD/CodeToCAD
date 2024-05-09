# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.

from abc import ABCMeta, abstractmethod


from typing import Self


from codetocad.interfaces.entity_interface import EntityInterface


class CameraInterface(EntityInterface, metaclass=ABCMeta):
    """
    Manipulate a camera object.
    """

    @abstractmethod
    def __init__(
        self, name: "str", description: "str| None" = None, native_instance=None
    ):

        self.name = name
        self.description = description
        self.native_instance = native_instance

    @abstractmethod
    def create_perspective(
        self,
    ) -> Self:
        """
        Create a perspective camera in the scene.
        """

        print(
            "create_perspective is called in an abstract method. Please override this method."
        )

        raise NotImplementedError()

    @abstractmethod
    def create_orthogonal(
        self,
    ) -> Self:
        """
        Create an orthogonal camera in the scene.
        """

        print(
            "create_orthogonal is called in an abstract method. Please override this method."
        )

        raise NotImplementedError()

    @abstractmethod
    def create_panoramic(
        self,
    ) -> Self:
        """
        Create a panorama camera in the scene.
        """

        print(
            "create_panoramic is called in an abstract method. Please override this method."
        )

        raise NotImplementedError()

    @abstractmethod
    def set_focal_length(self, length: "float") -> Self:
        """
        Set the focal length of the camera.
        """

        print(
            "set_focal_length is called in an abstract method. Please override this method."
        )

        raise NotImplementedError()
