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

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from . import EntityInterface


class LandmarkInterface(EntityInterface, metaclass=ABCMeta):
    """Landmarks are named positions on an entity."""

    name: str
    parent_entity: EntityOrItsName
    description: Optional[str] = None

    @abstractmethod
    def __init__(
        self,
        name: str,
        parent_entity: EntityOrItsName,
        description: Optional[str] = None,
        native_instance=None,
    ):
        super().__init__(
            name=name, description=description, native_instance=native_instance
        )
        self.name = name
        self.parent_entity = parent_entity
        self.description = description
        self.native_instance = native_instance

    @abstractmethod
    def get_landmark_entity_name(self) -> str:
        """
        Get the landmark object name in the scene, which may be different to the name of the landmark when it was first created. For example, the generated name may be {parentName}_{landmarkName}.
        """

        print(
            "get_landmark_entity_name is called in an abstract method. Please override this method."
        )
        raise NotImplementedError()

    @abstractmethod
    def get_parent_entity(self) -> "EntityInterface":
        """
        Get the name of the entity this landmark belongs to.
        """

        print(
            "get_parent_entity is called in an abstract method. Please override this method."
        )
        raise NotImplementedError()
