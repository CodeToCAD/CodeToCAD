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


capabilitiesToPyTest = f"capabilitiesToPyTest.j2"
capabilitiesToPyTestOut = f"{outputDir}/testsInterfaces"

with open(capabilitiesJson) as f:
    capabilities: dict = json.load(f)

templatesToGenerate = [
    (capabilitiesToPyInterface, capabilitiesToPyInterfaceOut, "Interface"),
    # (capabilitiesToPyProvider, capabilitiesToPyProviderOut),
    # (capabilitiesToPyTest, capabilitiesToPyTestOut)
]

templateLoader = jinja2.FileSystemLoader(searchpath=templatesDir)
templateEnv = jinja2.Environment(loader=templateLoader)

for template, output, suffix in templatesToGenerate:
    print("Generating", template)

    for className, methods in capabilities["capabilities"].items():
        template = templateEnv.get_template(template)
        output_from_parsed_template = template.render(
            dict(
                {
                    "className": className+suffix,
                    "methods": methods
                },
                **capabilities
            )
        )
        with open(output + f"/{className}{suffix}.py", "w") as fh:
            fh.write(output_from_parsed_template)

    print("Done")
