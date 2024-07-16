import ast
import ast_comments
import os
from argparse import ArgumentParser
from development.capabilities_json_to_python.capabilities_loader import (
    CapabilitiesLoader,
)

from codetocad.utilities.supported import supported  # noqa don't remove this
from codetocad.enums.support_level import SupportLevel  # noqa don't remove this


SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))

providers_path = f"{SCRIPT_DIR}/../providers/"


def get_provider_folder(provider_name: str):
    return providers_path + provider_name.lower() + f"/{provider_name.lower()}_provider"


def get_provider_file(provider_name: str, class_name: str):
    return get_provider_folder(provider_name) + "/" + class_name.lower() + ".py"


capabilities_loader = CapabilitiesLoader()


def get_class_by_name(class_name: str, definitions: list[ast_comments.stmt]):
    for definition in definitions:
        if isinstance(definition, ast_comments.ClassDef):
            if definition.name == class_name:
                return definition

    raise Exception(f"{class_name} does not exist in the definitions")


def get_function_by_name(function_name: str, definitions: list[ast_comments.stmt]):
    for definition in definitions:
        if isinstance(definition, ast_comments.FunctionDef):
            if definition.name == function_name:
                return definition

    return None


def get_provider_supported_decorators(provider_name: str):

    supporteds = {}
    for class_name in capabilities_loader.all_implementable_class_names:
        supporteds[class_name] = get_provider_class_supported_decorators(
            provider_name=provider_name, class_name=class_name
        )

    return supporteds


def get_provider_class_supported_decorators(provider_name: str, class_name: str):
    """
    Using AST, we'll read the @supported decorator information https://pypi.org/project/ast-comments/
    """

    provider_path = get_provider_file(provider_name, class_name)

    fp = open(provider_path, encoding="utf-8")
    provider_file_content = fp.read()
    fp.close()

    provider_definitions = ast_comments.parse(provider_file_content)

    provider_class = get_class_by_name(class_name, provider_definitions.body)

    method_names = capabilities_loader.get_implementable_method_names_for_class(
        class_name
    )

    supporteds = {}
    SUPPORTED_ARGS = ["supportedLevel", "notes", "versions"]
    for definition in provider_class.body:
        if isinstance(definition, ast_comments.FunctionDef):
            if definition.name[0] == "_":
                continue

            if definition.name not in method_names:
                continue

            for decorator in definition.decorator_list:
                dec_name = (
                    decorator.id if hasattr(decorator, "id") else decorator.func.id
                )
                if dec_name != "supported":
                    continue

                supported_metadata = {}

                for index, arg in enumerate(decorator.args):
                    name = (
                        arg.value.id
                        if isinstance(arg, ast.Attribute)
                        else SUPPORTED_ARGS[index]
                    )
                    value = arg.attr if isinstance(arg, ast.Attribute) else arg.value

                    supported_metadata[name] = value

                for arg in decorator.keywords:
                    name = arg.arg
                    value = arg.value.value
                    supported_metadata[name] = value

                supported_metadata["is_supported_or_partial"] = (
                    SupportLevel[supported_metadata["SupportLevel"]].value
                    >= SupportLevel.PARTIAL.value
                )

                supporteds[definition.name] = supported_metadata

    return supporteds


def main():
    parser = ArgumentParser()
    parser.add_argument(
        "-p",
        "--provider_name",
        type=str,
        help="The provider name in the providers folder.",
    )
    parser.add_argument(
        "-c",
        "--class_name",
        type=str,
        required=False,
        help="If passed, only this class_name will be parsed.",
    )
    args = parser.parse_args()

    provider_name = getattr(args, "provider_name", None)
    class_name = getattr(args, "class_name", None)

    if not provider_name:
        raise RuntimeError("--provider_name must be specified")

    supporteds = (
        get_provider_class_supported_decorators(
            provider_name=provider_name,
            class_name=class_name,
        )
        if class_name
        else get_provider_supported_decorators(
            provider_name=provider_name,
        )
    )

    print(supporteds)


if __name__ == "__main__":
    main()
