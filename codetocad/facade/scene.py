# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.
# Copy this file and remove this header to create a new CodeToCAD Provider.

from codetocad.codetocad_types import *
from codetocad.utilities import *
from codetocad.core import *
from codetocad.enums import *


from codetocad.interfaces.scene_interface import SceneInterface


from codetocad.interfaces.entity_interface import EntityInterface


class Scene:
    """
    Scene, camera, lighting, rendering, animation, simulation and GUI related functionality.

    NOTE: This is a facade-factory - calling this returns an instance of a registered provider.
    Register a provider using the `register()` method.
    """

    def __new__(
        cls, name: "str| None" = None, description: "str| None" = None
    ) -> SceneInterface:
        return cls._provider(name, description)

    @classmethod
    def register(cls, provider: SceneInterface):
        cls._provider = provider
