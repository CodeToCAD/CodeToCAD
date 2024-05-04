"""
A script to generate the CodeToCAD python files defined in template_utils.py::get_templates_to_generate() from capabilities.json + jinja2 templates.
"""

from development.capabilities_json_to_python.capabilities_loader import (
    CapabilitiesLoader,
)
from development.capabilities_json_to_python.template_utils import (
    TemplateArgs,
    get_jinja_environment,
    get_templates_to_generate,
)
from development.utilities import to_snake_case


def create_init_file(outpit_dir: str, class_names: list[str], file_name_suffix):
    with open(outpit_dir + "/__init__.py", "w") as handler:
        handler.write(
            """# THIS IS AN AUTO-GENERATED FILE. DO NOT CHANGE.\n
"""
        )

        for class_name in class_names:
            handler.write(
                f"from .{class_name.lower()}{'_'+file_name_suffix.lower() if file_name_suffix else ''} import {class_name}{file_name_suffix}\n"
            )


def create_register_method(outpit_dir: str, class_names: list[str]):
    with open(outpit_dir + "/register.py", "w") as handler:
        handler.write(
            """# THIS IS AN AUTO-GENERATED FILE. DO NOT CHANGE.\n
"""
        )
        for class_name in class_names:
            handler.write(f"from .{class_name.lower()} import {class_name}\n")
            handler.write(
                f"from codetocad.interfaces.{class_name.lower()}_interface import {class_name}Interface\n"
            )

        handler.write("def register():\n")

        for class_name in class_names:
            handler.write(
                f"    __import__('codetocad').providers.register({class_name}, {class_name}Interface)\n"
            )


def generate_template_for_class(
    class_name,
    capabilities_loader: CapabilitiesLoader,
    template_args: TemplateArgs,
):
    file_name = to_snake_case(f"{class_name}{template_args.suffix}")

    template = get_jinja_environment().get_template(template_args.template_path)

    output_from_parsed_template = template.render(
        dict(
            {
                "class_name": class_name,
                "template_args": template_args,
                "capabilities_loader": capabilities_loader,
            }
        )
    )
    with open(template_args.output_folder_path + f"/{file_name}.py", "w") as fh:
        fh.write(output_from_parsed_template)


def generate_all_templates(
    capabilities_loader: CapabilitiesLoader, templates_to_generate: list[TemplateArgs]
):
    for template_args in templates_to_generate:
        print("Generating", template_args.template_path)

        if template_args.generate_init_file_imports:
            class_names = capabilities_loader.all_class_names
            if (
                not template_args.generate_interface_only_capabilities_in_a_separate_file
            ):
                class_names = capabilities_loader.all_implementable_class_names
            create_init_file(
                template_args.output_folder_path,
                class_names,
                file_name_suffix=template_args.suffix,
            )
        else:
            create_init_file(
                template_args.output_folder_path, [], ""
            )  # Generate an empty __init__.py file

        if template_args.generate_registration_methods:
            create_register_method(
                template_args.output_folder_path,
                capabilities_loader.all_implementable_class_names,
            )

        for class_name in capabilities_loader.all_interface_only_class_names:
            if (
                not template_args.generate_interface_only_capabilities_in_a_separate_file
            ):
                continue

            generate_template_for_class(
                class_name=class_name,
                capabilities_loader=capabilities_loader,
                template_args=template_args,
            )

        for class_name in capabilities_loader.all_implementable_class_names:
            generate_template_for_class(
                class_name=class_name,
                capabilities_loader=capabilities_loader,
                template_args=template_args,
            )

        print("Done")


if __name__ == "__main__":
    generate_all_templates(
        capabilities_loader=CapabilitiesLoader(),
        templates_to_generate=get_templates_to_generate(),
    )
