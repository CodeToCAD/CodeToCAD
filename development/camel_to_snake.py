import ast
from dataclasses import dataclass, field
import os
from pathlib import Path
from argparse import ArgumentParser
from typing import List

from development.utilities import to_snake_case


def directory_to_snake_case(directory_path: str, replace_definitions_only: bool = False, overwrite: bool = True):
    # References https://stackoverflow.com/a/10378012
    pathlist = Path(directory_path).glob('**/*.py')
    for path in pathlist:
        path_in_str = str(path)

        if '__init__' in path_in_str:
            continue

        print(f"On {path_in_str}")

        file_to_snake_case(path_in_str, replace_definitions_only, overwrite)


@dataclass
class FileData:
    file_content: str
    definitions: List[ast.stmt] = field(default_factory=list)


def file_to_snake_case(filepath: str, replace_definitions_only: bool = False, overwrite: bool = True):
    '''
    Reads a python file, uses the AST module to read its symbols and replace method names and arg names with their snake_case counterparts. NOTE: Does not support nested classes, and possibly other overlooked nestings.

    replace_definitions_only flag determines if only the method definitions line is changed. NOTE: str.replace() is used to change all definitions in the file - which may incorrectly replace words that are not the method name or arg names.
    '''
    file_content = open(filepath, encoding='utf-8').read()

    definitions = ast.parse(file_content).body

    file_data = FileData(
        file_content=file_content,
        definitions=definitions
    )

    for definition in definitions:
        parse_definition(
            definition=definition,
            file_data=file_data,
            replace_definitions_only=replace_definitions_only
        )

    new_file = file_data.file_content

    if replace_definitions_only:
        new_file = ""

        for definition in definitions:
            new_file += ast.unparse(definition) + "\n"

    if overwrite:
        # camelcase the filename as well:
        _, filename = os.path.split(filepath)

        filepath_snake_case = filepath.replace(
            filename,
            to_snake_case(filename)
        )

        print(f"Writing to {filepath_snake_case}")

        if filepath_snake_case != filepath:
            os.remove(filepath)

        open(filepath_snake_case, 'w').write(new_file)
    else:
        print(new_file)


def parse_definition(definition: ast.stmt, file_data: FileData, replace_definitions_only: bool = False):
    if isinstance(definition,  ast.ClassDef):

        return class_to_snake_case(
            definition=definition,
            file_data=file_data,
            replace_definitions_only=replace_definitions_only
        )

    if isinstance(definition,  ast.FunctionDef):

        return method_to_snake_case(
            method=definition,
            file_data=file_data,
            replace_definitions_only=replace_definitions_only
        )

    print(f"Skipping {definition}")


def method_to_snake_case(method, file_data: FileData, replace_definitions_only: bool = False):

    method_name = getattr(method, "name", None)

    if not method_name:
        print(f"Skipping method {method}")
        return

    print(f"Parsing method: {method_name}")

    method_name_snake = to_snake_case(method.name)

    if replace_definitions_only:
        method.name = method_name_snake
    else:
        file_data.file_content = file_data.file_content.replace(
            method_name, method_name_snake)

    for arg in method.args.args:
        arg_name = arg.arg
        arg_name_snake = to_snake_case(arg.arg)

        if replace_definitions_only:
            arg.arg = arg_name_snake
        else:
            file_data.file_content = file_data.file_content.replace(
                arg_name, arg_name_snake)


def class_to_snake_case(definition: ast.stmt, file_data: FileData, replace_definitions_only: bool = False):
    definition_name = getattr(definition, "name", None)
    methods = getattr(definition, "body", [])

    print(f"Parsing class: {definition_name}")

    for method in methods:
        parse_definition(
            definition=method,
            file_data=file_data,
            replace_definitions_only=replace_definitions_only
        )


def main():
    parser = ArgumentParser()
    parser.add_argument('--replace_definitions_only', action='store_true',
                        help='''replace_definitions_only flag determines if only the method definitions line is changed. NOTE: str.replace() is used to change all definitions in the file - which may incorrectly replace words that are not the method name or arg names.
                        ''')
    parser.add_argument('-o', '--overwrite',
                        action='store_true', help='Overwrite source file.')
    parser.add_argument('-f', '--file', type=str,
                        required=False, help='Filepath to convert')
    parser.add_argument('-d', '--directory', type=str,
                        required=False, help='Directory to convert.')
    args = parser.parse_args()

    filepath = getattr(args, "file", None)
    directorypath = getattr(args, "directory", None)

    overwrite = getattr(args, "overwrite", False)
    replace_definitions_only = getattr(args, "replace_definitions_only", False)

    if filepath:
        return file_to_snake_case(filepath, replace_definitions_only, overwrite)

    if directorypath:
        return directory_to_snake_case(directorypath, replace_definitions_only, overwrite)

    raise RuntimeError("--file or --directory must be specified")


if __name__ == "__main__":
    main()
