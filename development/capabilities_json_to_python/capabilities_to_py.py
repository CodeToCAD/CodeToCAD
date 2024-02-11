from development.capabilities_json_to_python.capabilities_loader import (
    CapabilitiesLoader,
)
from development.capabilities_json_to_python.template_utils import (
    TemplateArgs,
    get_jinja_environment,
    get_templates_to_generate,
)
from development.utilities import to_snake_case


def create_init_file(outpit_dir: str):
    with open(outpit_dir + "/__init__.py", "w") as handler:
        handler.write(
            """# THIS IS AN AUTO-GENERATED FILE. DO NOT CHANGE.\n
"""
        )


def generate_template_for_class(
    class_name,
    capabilities_loader: CapabilitiesLoader,
    template_args: TemplateArgs,
):
    file_name = to_snake_case(f"{class_name}{template_args.suffix}")

    with open(template_args.output_folder_path + "/__init__.py", "a") as handler:
        handler.write(f"from .{file_name} import {class_name}{template_args.suffix}\n")

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

        create_init_file(template_args.output_folder_path)

        for class_name, methods in capabilities_loader.capabilities.items():
            if (
                not template_args.generate_interface_only_capabilities_in_a_separate_file
                and methods.get("is_interface_only", False) is True
            ):
                continue

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
