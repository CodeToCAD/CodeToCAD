# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.
# Copy this file and remove this header to create a new CodeToCAD Provider.

from codetocad.codetocad_types import *


from codetocad.providers import get_provider

from codetocad.interfaces.animation_interface import AnimationInterface


from codetocad.interfaces.entity_interface import EntityInterface


class Animation:
    """
    Animation related functionality.

    NOTE: This is a proxy-factory - calling this returns an instance of a registered provider.
    Register a provider using the `register()` method.
    """

    def __new__(
        cls,
    ) -> AnimationInterface:
        return get_provider(AnimationInterface)()  # type: ignore

    @staticmethod
    def default() -> "AnimationInterface":
        print(
            "default called",
        )

        return Animation()
