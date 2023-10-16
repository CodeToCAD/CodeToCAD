from copy import deepcopy
import re
import os
import json
pattern1 = re.compile(r'(.)([A-Z][a-z]+)')
pattern2 = re.compile(r'__([A-Z])')
pattern3 = re.compile(r'([a-z0-9])([A-Z])')


def to_snake_case(name):
    # references https://stackoverflow.com/a/1176023/9824103
    name = pattern1.sub(r'\1_\2', name)
    name = pattern2.sub(r'_\1', name)
    name = pattern3.sub(r'\1_\2', name)
    return name.lower()


script_dir, _ = os.path.split(__file__)

capabilities = json.load(
    open(f"{script_dir}/capabilities.json"))

# capabilities_new = json.loads(json.dumps(capabilities))

for className in capabilities["capabilities"].keys():
    methods = list(capabilities["capabilities"][className].keys())

    for method in methods:

        method_name_snake = to_snake_case(method)

        method_copy = deepcopy(
            capabilities["capabilities"][className][method]
        )

        del capabilities["capabilities"][className][method]

        capabilities["capabilities"][className][method_name_snake] = method_copy

        if "parameters" in capabilities["capabilities"][className][method_name_snake]:

            parameters = list(capabilities["capabilities"][className][method_name_snake]["parameters"].keys(
            ))

            for parameter in parameters:
                parameter_name_snake = to_snake_case(parameter)

                parameter_copy = deepcopy(
                    capabilities["capabilities"][className][method_name_snake]["parameters"][parameter]
                )

                del capabilities["capabilities"][className][method_name_snake]["parameters"][parameter]

                capabilities["capabilities"][className][method_name_snake]["parameters"][
                    parameter_name_snake] = parameter_copy


json.dump(capabilities, open(
    f"{script_dir}/capabilities_snake.json", "w"))
