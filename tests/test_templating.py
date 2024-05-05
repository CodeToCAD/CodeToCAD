import unittest

from development.capabilities_json_to_python.capabilities_loader import (
    CapabilitiesLoader,
)


class TestTemplating(unittest.TestCase):
    capabilies_loader = CapabilitiesLoader()

    def test_generate_methods(self):
        imports = self.capabilies_loader.generate_imports("Sketch", ["Sketch"])

        assert imports._codetocad_implementable_class_names == {
            "Landmark",
            "Wire",
            "Vertex",
        }
        assert imports._codetocad_interface_class_names == {
            "Projectable",
            "Importable",
            "Mirrorable",
            "Landmarkable",
            "Exportable",
            "Scalable",
            "Patternable",
        }

        imports = self.capabilies_loader.generate_imports("Part", ["Part"])

        assert imports._codetocad_implementable_class_names == {
            "Landmark",
            "Material",
        }

        assert imports._codetocad_interface_class_names == {
            "Exportable",
            "Booleanable",
            "Subdividable",
            "Scalable",
            "Importable",
            "Landmarkable",
            "Mirrorable",
            "Patternable",
        }

        imports = self.capabilies_loader.generate_imports("Edge", ["Edge"])

        assert imports._codetocad_implementable_class_names == {"Vertex", "Landmark"}
        assert imports._codetocad_interface_class_names == {
            "Projectable",
            "Patternable",
            "Subdividable",
            "Landmarkable",
            "Mirrorable",
        }

        imports = self.capabilies_loader.generate_imports("Wire", ["Wire"])

        assert imports._codetocad_implementable_class_names == {
            "Vertex",
            "Landmark",
            "Edge",
            "Part",
        }

        assert imports._codetocad_interface_class_names == {
            "Booleanable",
            "Landmarkable",
            "Patternable",
            "Mirrorable",
            "Projectable",
            "Subdividable",
        }

    def test_init_parameters(self):
        parameters = self.capabilies_loader.get_constructor_parameters_for_class(
            "Vertex"
        )

        has_default_value = False

        for parameter in parameters:
            if parameter.default_value is None and parameter.required:
                assert (
                    has_default_value is False
                ), "Argument with non-default value found after one with a default argument"
            else:
                has_default_value = True
