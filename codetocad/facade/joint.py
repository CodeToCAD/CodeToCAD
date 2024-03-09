# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.
# Copy this file and remove this header to create a new CodeToCAD Provider.

from codetocad.codetocad_types import *
from codetocad.utilities import *
from codetocad.core import *
from codetocad.enums import *


from codetocad.interfaces.joint_interface import JointInterface


from codetocad.interfaces.entity_interface import EntityInterface


class Joint:
    """
    Joints define the relationships and constraints between entities.

    NOTE: This is a facade-factory - calling this returns an instance of a registered provider.
    Register a provider using the `register()` method.
    """

    def __new__(
        cls, entity1: "EntityOrItsName", entity2: "EntityOrItsName"
    ) -> JointInterface:
        return cls._provider(entity1, entity2)

    @classmethod
    def register(cls, provider: JointInterface):
        cls._provider = provider
