# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.
# Copy this file and remove this header to create a new CodeToCAD Provider.


from codetocad.interfaces.material_interface import MaterialInterface

from codetocad.providers import get_provider


def create_material(name: "str", description: "str| None" = None) -> MaterialInterface:
    """
    Materials affect the appearance and simulation properties of the parts.

    NOTE: This is a factory - calling this returns an instance of a registered provider.
    Register a provider using the `register()` method.
    """
    return get_provider(MaterialInterface)(name, description)  # type: ignore


def get_preset_material(material_name: "PresetMaterial") -> "MaterialInterface":
    return get_provider(MaterialInterface).get_preset(material_name)
