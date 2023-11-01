import jinja2
import os
import json

from development.utilities import to_snake_case


SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))

output_dir = f"{SCRIPT_DIR}/../../codetocad/"
docs = f"{SCRIPT_DIR}/../../docs/"
templates_dir = f"{SCRIPT_DIR}/templates"

capabilities_json = f"{SCRIPT_DIR}/../../codetocad/capabilities.json"

capabilities_to_py_interface = "capabilities_to_py_interface.j2"
capabilities_to_py_interface_out = f"{output_dir}/interfaces"


capabilities_to_py_provider = "capabilities_to_py_provider.j2"
capabilities_to_py_provider_out = f"{output_dir}/providers_sample"


capabilities_to_py_test_interface = "capabilities_to_py_test_interface.j2"
capabilities_to_py_test_interface_out = f"{output_dir}/tests_interfaces"


capabilities_to_py_test = "capabilities_to_py_test.j2"
capabilities_to_py_test_out = f"{output_dir}/tests_sample"

with open(capabilities_json) as f:
    capabilities: dict = json.load(f)


def make_template_args(
    template_path: str,
    output_path: str,
    suffix: str,
    generate_interface_only_capabilities_in_a_separate_file: bool,
):
    return (
        template_path,
        output_path,
        suffix,
        generate_interface_only_capabilities_in_a_separate_file,
    )


templates_to_generate = [
    make_template_args(
        capabilities_to_py_interface,
        capabilities_to_py_interface_out,
        "Interface",
        True,
    ),
    make_template_args(
        capabilities_to_py_provider, capabilities_to_py_provider_out, "", False
    ),
    make_template_args(
        capabilities_to_py_test_interface,
        capabilities_to_py_test_interface_out,
        "TestInterface",
        True,
    ),
    make_template_args(
        capabilities_to_py_test, capabilities_to_py_test_out, "Test", False
    ),
]

template_loader = jinja2.FileSystemLoader(searchpath=templates_dir)
template_env = jinja2.Environment(loader=template_loader)


def create_init_file(outpit_dir: str):
    with open(outpit_dir + "/__init__.py", "w") as handler:
        handler.write(
            """# THIS IS AN AUTO-GENERATED FILE. DO NOT CHANGE.\n
"""
        )


for (
    template,
    output,
    suffix,
    generate_interface_only_capabilities_in_a_separate_file,
) in templates_to_generate:
    print("Generating", template)

    create_init_file(output)

    all_classes: dict[str, dict] = capabilities["capabilities"]
    all_class_names = all_classes.keys()
    for class_name, methods in all_classes.items():
        file_name = to_snake_case(f"{class_name}{suffix}")

        if (
            not generate_interface_only_capabilities_in_a_separate_file
            and methods.get("is_interface_only", False) is True
        ):
            continue

        with open(output + "/__init__.py", "a") as handler:
            handler.write(f"from .{file_name} import {class_name}{suffix}\n")

        template = template_env.get_template(template)
        output_from_parsed_template = template.render(
            dict(
                {
                    "className": class_name,
                    "classNameSuffix": suffix,
                    "methods": methods,
                    "generate_interface_only_capabilities_in_a_separate_file": generate_interface_only_capabilities_in_a_separate_file,
                    "all_codetocad_class_names": all_class_names,
                    "all_classes": all_classes,
                },
                **capabilities,
            )
        )
        with open(output + f"/{file_name}.py", "w") as fh:
            fh.write(output_from_parsed_template)

    print("Done")
