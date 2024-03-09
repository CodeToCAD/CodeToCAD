# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.
# Copy this file and remove this header to create a new CodeToCAD Provider.

from codetocad.codetocad_types import *
from codetocad.utilities import *
from codetocad.core import *
from codetocad.enums import *


from codetocad.interfaces.render_interface import RenderInterface


from codetocad.interfaces.camera_interface import CameraInterface


class Render:
    """
    Render the scene and export images or videos.

    NOTE: This is a facade-factory - calling this returns an instance of a registered provider.
    Register a provider using the `register()` method.
    """

    def __new__(
        cls,
    ) -> RenderInterface:
        return cls._provider()

    @classmethod
    def register(cls, provider: RenderInterface):
        cls._provider = provider
