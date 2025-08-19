import os
from pathlib import Path
from types import FunctionType
import inspect


def write_function_code_to_file(
    func: FunctionType,
    output_path: str,
    prepend_code: str,
    append_code: str,
    args: list,
    kwargs: dict,
):
    """
    To simplify the UX while executing CodeToCAD code, the user's script will be bundled into a single .py file and saved to disk. It can then be subsequently be consumed by reloading it from disk.

    args and kwargs must be serializable.. even then, mileage may vary.
    """
    # function_filename_full = inspect.getsourcefile(func)
    # if not function_filename_full:
    #     raise Exception(f"Could not find source file for {func.__name__}.")

    filename = inspect.getfile(func)
    script_directory = f"{Path(filename).parent.absolute()}"

    # Get the directory and base filename without extension
    directory = os.path.dirname(filename)
    base_filename = os.path.basename(filename).replace(".py", "")

    # If the file is in the current working directory or a simple module
    if directory == os.getcwd() or "" in directory:  # Simplified check
        module_name = base_filename
    else:
        # For more complex package structures, you'd need to determine the package root
        # and build the relative path from there. This is a placeholder.
        module_name = base_filename  # Example: assuming it's a direct import

    import_statement = f"from {module_name} import {func.__name__}"

    with open(output_path, "w") as f:
        f.write(prepend_code)
        f.write(
            f"""
import sys
sys.path.append('{script_directory}')
{import_statement}
"""
        )
        f.write(
            f"""
if __name__ == "__main__":
    {func.__name__}(
    {"'" if len(args) >0 else ""}{"',".join(args) if len(args) > 0 else ''}{"'" if len(args) == 1 else ""}{"," if len(args) >0  and len(kwargs) >0 else ""}
    {",".join([f"{k}='{v}'" for k, v in kwargs.items()]) if kwargs else ""})  # Call the main function
"""
        )
        f.write(append_code)
