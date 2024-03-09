# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.
# Copy this file and remove this header to create a new CodeToCAD Provider.

from codetocad.codetocad_types import *
from codetocad.utilities import *
from codetocad.core import *
from codetocad.enums import *


from codetocad.interfaces.camera_interface import CameraInterface


from codetocad.interfaces.entity_interface import EntityInterface


class Camera:
    """
    Manipulate a camera object.

    NOTE: This is a facade-factory - calling this returns an instance of a registered provider.
    Register a provider using the `register()` method.
    """

    def __new__(
        cls, name: "str", description: "str| None" = None, native_instance=None
    ) -> CameraInterface:
        return cls._provider(name, description, native_instance)

    @classmethod
    def register(cls, provider: CameraInterface):
        cls._provider = provider
