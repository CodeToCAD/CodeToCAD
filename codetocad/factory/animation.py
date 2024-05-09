# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.
# Copy this file and remove this header to create a new CodeToCAD Provider.


from codetocad.interfaces.animation_interface import AnimationInterface

from codetocad.providers import get_provider


def create_animation() -> AnimationInterface:
    """
    Animation related functionality.

    NOTE: This is a factory - calling this returns an instance of a registered provider.
    Register a provider using the `register()` method.
    """
    return get_provider(AnimationInterface)()  # type: ignore


def default_animation() -> "AnimationInterface":
    return get_provider(AnimationInterface).default()
