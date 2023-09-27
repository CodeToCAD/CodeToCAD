import jinja2
import os
import json


SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))

outputDir = f"{SCRIPT_DIR}/../../CodeToCAD/"
docs = f"{SCRIPT_DIR}/../../docs/"
templatesDir = f"{SCRIPT_DIR}/templates"

capabilitiesJson = f"{SCRIPT_DIR}/../../CodeToCAD/capabilities.json"

capabilitiesToPyInterface = f"capabilitiesToPyInterface.j2"
capabilitiesToPyInterfaceOut = f"{outputDir}/interfaces"


capabilitiesToPyProvider = f"capabilitiesToPyProvider.j2"
capabilitiesToPyProviderOut = f"{outputDir}/providersSample"


capabilitiesToPyTestInterface = f"capabilitiesToPyTestInterface.j2"
capabilitiesToPyTestInterfaceOut = f"{outputDir}/testsInterfaces"


capabilitiesToPyTest = f"capabilitiesToPyTest.j2"
capabilitiesToPyTestOut = f"{outputDir}/testsSample"

with open(capabilitiesJson) as f:
    capabilities: dict = json.load(f)

templatesToGenerate = [
    (capabilitiesToPyInterface, capabilitiesToPyInterfaceOut, "Interface"),
    (capabilitiesToPyProvider, capabilitiesToPyProviderOut, ""),
    (capabilitiesToPyTestInterface, capabilitiesToPyTestInterfaceOut, "TestInterface"),
    (capabilitiesToPyTest, capabilitiesToPyTestOut, "Test")
]

templateLoader = jinja2.FileSystemLoader(searchpath=templatesDir)
templateEnv = jinja2.Environment(loader=templateLoader)


def createInitFile(outputDir: str):
    with open(outputDir + "/__init__.py", "w") as handler:
        handler.write(
            '''# THIS IS AN AUTO-GENERATED FILE. DO NOT CHANGE.\n
''')


for template, output, suffix in templatesToGenerate:
    print("Generating", template)

    createInitFile(output)

    for className, methods in capabilities["capabilities"].items():

        with open(output + "/__init__.py", "a") as handler:
            handler.write(
                f"from .{className}{suffix} import {className}{suffix}\n")

        template = templateEnv.get_template(template)
        output_from_parsed_template = template.render(
            dict(
                {
                    "className": className,
                    "classNameSuffix": suffix,
                    "methods": methods
                },
                **capabilities
            )
        )
        with open(output + f"/{className}{suffix}.py", "w") as fh:
            fh.write(output_from_parsed_template)

    print("Done")
