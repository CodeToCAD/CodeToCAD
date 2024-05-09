# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.
# Copy this file and remove this header to create a new CodeToCAD Provider.


from codetocad.interfaces.scene_interface import SceneInterface

from codetocad.providers import get_provider


def create_scene(
    name: "str| None" = None, description: "str| None" = None
) -> SceneInterface:
    """
    Scene, camera, lighting, rendering, animation, simulation and GUI related functionality.

    NOTE: This is a factory - calling this returns an instance of a registered provider.
    Register a provider using the `register()` method.
    """
    return get_provider(SceneInterface)(name, description)  # type: ignore


def default_scene() -> "SceneInterface":
    return get_provider(SceneInterface).default()
