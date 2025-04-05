import ast_comments
import os
from argparse import ArgumentParser
import shutil
from development.capabilities_json_to_python.capabilities_loader import (
    CapabilitiesLoader,
)
from development.capabilities_json_to_python.capabilities_to_py import (
    create_register_method,
)

from codetocad.utilities.supported import supported  # noqa don't remove this
from codetocad.enums.support_level import SupportLevel  # noqa don't remove this


SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))

sample_provider_path = f"{SCRIPT_DIR}/../providers/sample/"
providers_path = f"{SCRIPT_DIR}/../providers/"


def get_log_markdown_file(provider_name: str):
    return f"{providers_path}/{provider_name.lower()}/update_providers_changelog.md"


def get_provider_folder(provider_name: str):
    return providers_path + provider_name.lower() + f"/{provider_name.lower()}_provider"


def get_provider_file(provider_name: str, class_name: str):
    return get_provider_folder(provider_name) + "/" + class_name.lower() + ".py"


def get_sample_file(class_name: str):
    return sample_provider_path + class_name.lower() + ".py"


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


def update_provider_directory(
    provider_name: str,
    is_remove_non_compliant_methods=True,
    is_dump_imports: bool = True,
    is_write: bool = True,
):
    shutil.copy(
        get_sample_file("__init__"), get_provider_file(provider_name, "__init__")
    )

    for class_name in capabilities_loader.all_implementable_class_names:
        update_provider_file(
            provider_name=provider_name,
            class_name=class_name,
            is_remove_non_compliant_methods_and_add_supported_decorator=is_remove_non_compliant_methods,
            is_dump_imports=is_dump_imports,
            is_write=is_write,
        )


def update_provider_file(
    provider_name: str,
    class_name: str,
    is_remove_non_compliant_methods_and_add_supported_decorator=True,
    is_dump_imports: bool = True,
    is_write: bool = True,
):
    """
    Quick and dirty semi-automatic updating of class and method definitions.
    There is no trivial way to do this correctly and accurately, but we will attempt to preserve the original provider file via https://pypi.org/project/ast-comments/

    `is_remove_non_compliant_methods` - if True, then all methods that are not sunder or dunder or @override decorated will be removed.
    `is_dump_imports` - if True, then the import statements from the sample file will be dumped at the top of the provider file. This may cause conflicts or duplicates.
    """

    provider_path = get_provider_file(provider_name, class_name)

    if not os.path.exists(provider_path):
        shutil.copyfile(get_sample_file(class_name), provider_path)
        return

    fp = open(get_sample_file(class_name), encoding="utf-8")
    sample_file_content = fp.read()
    fp.close()

    fp = open(provider_path, encoding="utf-8")
    provider_file_content = fp.read()
    fp.close()

    provider_definitions = ast_comments.parse(provider_file_content)

    sample_definitions = ast_comments.parse(sample_file_content)

    provider_class = get_class_by_name(class_name, provider_definitions.body)
    sample_class = get_class_by_name(class_name, sample_definitions.body)

    provider_class.bases = sample_class.bases

    log_markdown_file_content = (
        f"## `{provider_name}.{class_name}` Additions and Deletions:\n\n"
    )

    for definition in sample_class.body:
        if isinstance(definition, ast_comments.FunctionDef):
            provider_function = get_function_by_name(
                definition.name, provider_class.body
            )

            if provider_function is None:
                provider_class.body.append(definition)

                log_markdown_file_content += f"""
- Added:
    ```python
    {ast_comments.unparse(definition)}
    ```
"""
                continue

            provider_function.args = definition.args
            provider_function.returns = definition.returns

            decorators = [
                dec.id if hasattr(dec, "id") else dec.func.id
                for dec in provider_function.decorator_list
            ]
            if not ("override" in decorators):
                provider_function.decorator_list = definition.decorator_list

    if is_dump_imports:
        count_dumps = 1
        provider_imports = []
        for definition in provider_definitions.body:
            if isinstance(definition, ast_comments.ImportFrom):
                provider_imports.append(ast_comments.unparse(definition))
        for definition in sample_definitions.body:
            if isinstance(definition, ast_comments.ImportFrom):
                if definition.module and "providers.sample" in definition.module:
                    # This is niche logic; if any of the imports reference sample provider specifically, change the module to point to this provider_name instead.
                    definition.module = definition.module.replace(
                        "providers.sample",
                        f"providers.{provider_name.lower()}.{provider_name.lower()}_provider",
                    )

                if ast_comments.unparse(definition) in provider_imports:
                    continue

                provider_definitions.body.insert(count_dumps, definition)
                count_dumps += 1

                log_markdown_file_content += (
                    f"- Added: `{ast_comments.unparse(definition)}`\n\n"
                )

    if is_remove_non_compliant_methods_and_add_supported_decorator:
        method_names = capabilities_loader.get_implementable_method_names_for_class(
            class_name
        )
        for definition in provider_class.body:
            if isinstance(definition, ast_comments.FunctionDef):
                if definition.name[0] == "_":
                    continue
                decorators = [
                    dec.id if hasattr(dec, "id") else dec.func.id
                    for dec in definition.decorator_list
                ]
                if "override" in decorators:
                    continue
                if "supported" not in decorators and definition.name in method_names:
                    definition.decorator_list.append(
                        ast_comments.ast.parse("supported(SupportLevel.UNSUPPORTED)")
                        .body[0]
                        .value
                    )
                if definition.name not in method_names:
                    provider_class.body.remove(definition)
                    log_markdown_file_content += f"""
- Deleted:
    ```python
    {ast_comments.unparse(definition)}
    ```
"""

    new_file = ast_comments.unparse(provider_definitions)

    if is_write:
        print(f"Writing to {provider_path}")

        with open(provider_path, "w") as fp:
            fp.write(new_file)

        with open(
            get_log_markdown_file(provider_name),
            "a",
        ) as fp:
            fp.write(log_markdown_file_content)
    else:
        print(new_file)
        print(log_markdown_file_content)


def main():
    parser = ArgumentParser()
    parser.add_argument(
        "-p",
        "--provider_name",
        type=str,
        help="The provider name in the providers folder.",
    )
    parser.add_argument(
        "-w", "--is_write", action="store_true", help="is_write source file to disk."
    )
    parser.add_argument(
        "-c",
        "--class_name",
        type=str,
        required=False,
        help="If passed, only this class_name will be updated.",
    )
    args = parser.parse_args()

    provider_name = getattr(args, "provider_name", None)
    class_name = getattr(args, "class_name", None)

    is_write = getattr(args, "is_write", False)

    if not provider_name:
        raise RuntimeError("--provider_name must be specified")

    try:
        os.remove(get_log_markdown_file(provider_name))
    except:  # noqa
        ...

    if class_name:
        return update_provider_file(
            provider_name=provider_name,
            class_name=class_name,
            is_remove_non_compliant_methods_and_add_supported_decorator=True,
            is_dump_imports=True,
            is_write=is_write,
        )

    update_provider_directory(
        provider_name=provider_name,
        is_remove_non_compliant_methods=True,
        is_dump_imports=True,
        is_write=is_write,
    )

    create_register_method(
        get_provider_folder(provider_name),
        capabilities_loader.all_implementable_class_names,
    )


if __name__ == "__main__":
    main()
