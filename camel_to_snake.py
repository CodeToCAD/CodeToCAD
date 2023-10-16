import ast
import os
import re
from pathlib import Path
from argparse import ArgumentParser


def directory_to_snake_case(directory_path: str, replace_definitions_only: bool = False, overwrite: bool = True):
    # References https://stackoverflow.com/a/10378012
    pathlist = Path(directory_path).glob('**/*.py')
    for path in pathlist:
        path_in_str = str(path)

        if '__init__' in path_in_str:
            continue

        print(f"On {path_in_str}")

        file_to_snake_case(path_in_str, replace_definitions_only, overwrite)


def file_to_snake_case(filepath: str, replace_definitions_only: bool = False, overwrite: bool = True):
    '''
    Reads a python file, uses the AST module to read its symbols and replace method names and arg names with their snake_case counterparts. NOTE: Does not support nested classes, and possibly other overlooked nestings.

    replace_definitions_only flag determines if only the method definitions line is changed. NOTE: str.replace() is used to change all definitions in the file - which may incorrectly replace words that are not the method name or arg names.
    '''
    pattern1 = re.compile(r'(.)([A-Z][a-z]+)')
    pattern2 = re.compile(r'__([A-Z])')
    pattern3 = re.compile(r'([a-z0-9])([A-Z])')

    def to_snake_case(name):
        # references https://stackoverflow.com/a/1176023/9824103
        name = pattern1.sub(r'\1_\2', name)
        name = pattern2.sub(r'_\1', name)
        name = pattern3.sub(r'\1_\2', name)
        return name.lower()

    file = open(filepath, encoding='utf-8').read()

    # We're going to assume the file module is the last index:
    file_module = ast.parse(file).body[-1]

    module_name = getattr(file_module, "name", None)
    methods = getattr(file_module, "body", [])

    print(f"Parsing module: {module_name}")

    for method in methods:
        method_name = getattr(method, "name", None)

        if not method_name:
            print(f"Skipping method {method}")
            continue

        method_name_snake = to_snake_case(method.name)

        if replace_definitions_only:
            method.name = method_name_snake
        else:
            file = file.replace(method_name, method_name_snake)

        for arg in method.args.args:
            arg_name = arg.arg
            arg_name_snake = to_snake_case(arg.arg)

            if replace_definitions_only:
                arg.arg = arg_name_snake
            else:
                file = file.replace(arg_name, arg_name_snake)

    new_file = file

    if replace_definitions_only:
        new_file = ast.unparse(file_module)

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
