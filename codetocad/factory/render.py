# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.
# Copy this file and remove this header to create a new CodeToCAD Provider.


from codetocad.interfaces.render_interface import RenderInterface

from codetocad.providers import get_provider


from codetocad.interfaces.camera_interface import CameraInterface


def create_render() -> RenderInterface:
    """
    Render the scene and export images or videos.

    NOTE: This is a factory - calling this returns an instance of a registered provider.
    Register a provider using the `register()` method.
    """
    return get_provider(RenderInterface)()  # type: ignore
