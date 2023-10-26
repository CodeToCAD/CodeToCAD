import jinja2
import os
import json

from development.utilities import to_snake_case


SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))

outputDir = f"{SCRIPT_DIR}/../../codetocad/"
docs = f"{SCRIPT_DIR}/../../docs/"
templatesDir = f"{SCRIPT_DIR}/templates"

capabilitiesJson = f"{SCRIPT_DIR}/../../codetocad/capabilities.json"

capabilities_to_py_interface = f"capabilities_to_py_interface.j2"
capabilities_to_py_interface_out = f"{outputDir}/interfaces"


capabilities_to_py_provider = f"capabilities_to_py_provider.j2"
capabilities_to_py_provider_out = f"{outputDir}/providers_sample"


capabilities_to_py_test_interface = f"capabilities_to_py_test_interface.j2"
capabilities_to_py_test_interface_out = f"{outputDir}/tests_interfaces"


capabilities_to_py_test = f"capabilities_to_py_test.j2"
capabilities_to_py_test_out = f"{outputDir}/tests_sample"

with open(capabilitiesJson) as f:
    capabilities: dict = json.load(f)

templatesToGenerate = [
    (capabilities_to_py_interface, capabilities_to_py_interface_out, "Interface"),
    (capabilities_to_py_provider, capabilities_to_py_provider_out, ""),
    (
        capabilities_to_py_test_interface,
        capabilities_to_py_test_interface_out,
        "TestInterface",
    ),
    (capabilities_to_py_test, capabilities_to_py_test_out, "Test"),
]

templateLoader = jinja2.FileSystemLoader(searchpath=templatesDir)
templateEnv = jinja2.Environment(loader=templateLoader)


def createInitFile(outputDir: str):
    with open(outputDir + "/__init__.py", "w") as handler:
        handler.write(
            """# THIS IS AN AUTO-GENERATED FILE. DO NOT CHANGE.\n
"""
        )


for template, output, suffix in templatesToGenerate:
    print("Generating", template)

    createInitFile(output)

    for className, methods in capabilities["capabilities"].items():
        file_name = to_snake_case(f"{className}{suffix}")

        with open(output + "/__init__.py", "a") as handler:
            handler.write(f"from .{file_name} import {className}{suffix}\n")

        template = templateEnv.get_template(template)
        output_from_parsed_template = template.render(
            dict(
                {"className": className, "classNameSuffix": suffix, "methods": methods},
                **capabilities,
            )
        )
        with open(output + f"/{file_name}.py", "w") as fh:
            fh.write(output_from_parsed_template)

    print("Done")
