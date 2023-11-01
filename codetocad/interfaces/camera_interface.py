# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.

from typing import Optional
from abc import ABCMeta, abstractmethod

from codetocad.codetocad_types import *
from codetocad.utilities import *
from codetocad.core import *
from codetocad.enums import *


from . import EntityInterface


class CameraInterface(EntityInterface, metaclass=ABCMeta):
    """Manipulate a camera object."""

    name: str
    description: Optional[str] = None

    @abstractmethod
    def __init__(
        self, name: str, description: Optional[str] = None, native_instance=None
    ):
        super().__init__(
            name=name, description=description, native_instance=native_instance
        )
        self.name = name
        self.description = description
        self.native_instance = native_instance

    @abstractmethod
    def create_perspective(self):
        """
        Create a perspective camera in the scene.
        """

        print(
            "create_perspective is called in an abstract method. Please override this method."
        )
        return self

    @abstractmethod
    def create_orthogonal(self):
        """
        Create an orthogonal camera in the scene.
        """

        print(
            "create_orthogonal is called in an abstract method. Please override this method."
        )
        return self

    @abstractmethod
    def set_focal_length(self, length: float):
        """
        Set the focal length of the camera.
        """

        print(
            "set_focal_length is called in an abstract method. Please override this method."
        )
        return self
