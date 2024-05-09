# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.

from abc import ABCMeta, abstractmethod


from typing import Self


from codetocad.interfaces.entity_interface import EntityInterface


class AnimationInterface(metaclass=ABCMeta):
    """
    Animation related functionality.
    """

    @staticmethod
    def default() -> "AnimationInterface":
        """
        Get an Animation instance for the current scene.
        """

        print("default is called in an abstract method. Please override this method.")

        raise NotImplementedError()

    @abstractmethod
    def set_frame_start(self, frame_number: "int") -> Self:
        """
        Set the start animation frame in the scene.
        """

        print(
            "set_frame_start is called in an abstract method. Please override this method."
        )

        raise NotImplementedError()

    @abstractmethod
    def set_frame_end(self, frame_number: "int") -> Self:
        """
        Set the end animation frame in the scene.
        """

        print(
            "set_frame_end is called in an abstract method. Please override this method."
        )

        raise NotImplementedError()

    @abstractmethod
    def set_frame_current(self, frame_number: "int") -> Self:
        """
        Set the current animation frame in the scene.
        """

        print(
            "set_frame_current is called in an abstract method. Please override this method."
        )

        raise NotImplementedError()

    @abstractmethod
    def create_key_frame_location(
        self, entity: "str|EntityInterface", frame_number: "int"
    ) -> Self:
        """
        Create an animation key-frame using the location of the entity.
        """

        print(
            "create_key_frame_location is called in an abstract method. Please override this method."
        )

        raise NotImplementedError()

    @abstractmethod
    def create_key_frame_rotation(
        self, entity: "str|EntityInterface", frame_number: "int"
    ) -> Self:
        """
        Create an animation key-frame using the rotation of the entity.
        """

        print(
            "create_key_frame_rotation is called in an abstract method. Please override this method."
        )

        raise NotImplementedError()
