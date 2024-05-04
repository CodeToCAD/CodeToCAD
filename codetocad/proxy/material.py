# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.
# Copy this file and remove this header to create a new CodeToCAD Provider.

from codetocad.codetocad_types import *


from codetocad.providers import get_provider

from codetocad.interfaces.material_interface import MaterialInterface


class Material:
    """
    Materials affect the appearance and simulation properties of the parts.

    NOTE: This is a proxy-factory - calling this returns an instance of a registered provider.
    Register a provider using the `register()` method.
    """

    def __new__(cls, name: "str", description: "str| None" = None) -> MaterialInterface:
        return get_provider(MaterialInterface)(name, description)  # type: ignore

    @staticmethod
    def get_preset(material_name: "PresetMaterial") -> "MaterialInterface":
        print("get_preset called", f": {material_name}")

        return Material("mat")
