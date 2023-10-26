import jinja2
import os
import json


SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))

docs = f"{SCRIPT_DIR}/../../docs/"
templatesDir = f"{SCRIPT_DIR}/templates"

examplesJson = f"{SCRIPT_DIR}/../../examples/examples.json"

examples_json_to_htmlTemplate = f"examples_json_to_html.j2"
examples_json_to_htmlOut = f"{docs}/examples.html"

examplesList = json.load(open(examplesJson))
for example in examplesList:
    codeFilepath = example["codeFilepath"]
    codeFilepath = f"{SCRIPT_DIR}/../../examples/{codeFilepath}"
    example["code"] = "\n" + "\n".join(open(codeFilepath).readlines())

templatesToGenerate = ((examples_json_to_htmlTemplate, examples_json_to_htmlOut),)

templateLoader = jinja2.FileSystemLoader(searchpath=templatesDir)
templateEnv = jinja2.Environment(loader=templateLoader)

for template, output in templatesToGenerate:
    print("Generating", template)

    template = templateEnv.get_template(template)
    output_from_parsed_template = template.render(**{"examples": examplesList})
    with open(output, "w") as fh:
        fh.write(output_from_parsed_template)

    print("Done")
