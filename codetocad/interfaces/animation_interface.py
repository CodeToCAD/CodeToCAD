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


class AnimationInterface(metaclass=ABCMeta):
    """Animation related functionality."""

    @abstractmethod
    def __init__(self):
        pass

    @staticmethod
    def default() -> "AnimationInterface":
        raise RuntimeError()

    @abstractmethod
    def set_frame_start(self, frame_number: "int"):
        """
        Set the start animation frame in the scene.
        """

        print(
            "set_frame_start is called in an abstract method. Please override this method."
        )
        return self

    @abstractmethod
    def set_frame_end(self, frame_number: "int"):
        """
        Set the end animation frame in the scene.
        """

        print(
            "set_frame_end is called in an abstract method. Please override this method."
        )
        return self

    @abstractmethod
    def set_frame_current(self, frame_number: "int"):
        """
        Set the current animation frame in the scene.
        """

        print(
            "set_frame_current is called in an abstract method. Please override this method."
        )
        return self

    @abstractmethod
    def create_key_frame_location(self, entity: EntityOrItsName, frame_number: "int"):
        """
        Create an animation key-frame using the location of the entity.
        """

        print(
            "create_key_frame_location is called in an abstract method. Please override this method."
        )
        return self

    @abstractmethod
    def create_key_frame_rotation(self, entity: EntityOrItsName, frame_number: "int"):
        """
        Create an animation key-frame using the rotation of the entity.
        """

        print(
            "create_key_frame_rotation is called in an abstract method. Please override this method."
        )
        return self
