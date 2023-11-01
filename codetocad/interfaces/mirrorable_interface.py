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


class MirrorableInterface(metaclass=ABCMeta):
    """An entity that can be mirrored."""

    @abstractmethod
    def mirror(
        self,
        mirror_across_entity: EntityOrItsName,
        axis: AxisOrItsIndexOrItsName,
        resulting_mirrored_entity_name: Optional[str] = None,
    ):
        """
        Mirror an existing entity with respect to a landmark. If a name is provided, the mirror becomes a separate entity.
        """

        print("mirror is called in an abstract method. Please override this method.")
        return self
