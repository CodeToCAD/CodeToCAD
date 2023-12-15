# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.

from typing import Optional
from abc import ABCMeta, abstractmethod

from codetocad.codetocad_types import *
from codetocad.utilities import *
from codetocad.core import *
from codetocad.enums import *


from codetocad.interfaces import ProjectableInterface

from . import EntityInterface

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from . import EntityInterface


class VertexInterface(EntityInterface, ProjectableInterface, metaclass=ABCMeta):
    """A single point in space, or a control point."""

    location: "Point"
    parent_entity: Optional[EntityOrItsName] = None

    @abstractmethod
    def __init__(
        self,
        location: "Point",
        name: str,
        parent_entity: Optional[EntityOrItsName] = None,
        description: Optional[str] = None,
        native_instance=None,
    ):
        super().__init__(
            name=name, description=description, native_instance=native_instance
        )
        self.location = location
        self.parent_entity = parent_entity
        self.name = name
        self.description = description
        self.native_instance = native_instance

    @abstractmethod
    def get_control_points(self, parameter="") -> "list[VertexInterface]":
        """
        Get a vertex's curve control points. This may not be applicable in several situations.
        """

        print(
            "get_control_points is called in an abstract method. Please override this method."
        )
        raise NotImplementedError()
