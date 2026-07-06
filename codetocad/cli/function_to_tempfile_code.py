import ast
import inspect
import textwrap
from types import FunctionType
from typing import Set, Dict


class FunctionCallCollector(ast.NodeVisitor):
    def __init__(self):
        self.called_functions: Set[str] = set()

    def visit_Call(self, node: ast.Call):
        if isinstance(node.func, ast.Name):
            self.called_functions.add(node.func.id)
        elif isinstance(node.func, ast.Attribute):
            # Skip method calls for now (e.g., obj.method()) — we assume those are built-in or external
            pass
        self.generic_visit(node)


def get_all_user_defined_functions(func: FunctionType) -> dict[str, FunctionType]:
    """
    Return a dict of all user-defined functions accessible from the given function's global context.
    """
    global_scope = func.__globals__
    return {
        name: val
        for name, val in global_scope.items()
        if isinstance(val, FunctionType)
        and inspect.getmodule(val) == inspect.getmodule(func)
    }


def collect_called_user_functions(func: FunctionType) -> Set[FunctionType]:
    """
    Collect all user-defined functions called directly or indirectly by `func`.
    """
    seen: Set[str] = set()
    to_process = [func]
    collected: Set[FunctionType] = set()
    available_functions = get_all_user_defined_functions(func)

    while to_process:
        current = to_process.pop()
        if current.__name__ in seen:
            continue
        seen.add(current.__name__)
        collected.add(current)

        try:
            source = inspect.getsource(current)
        except (OSError, TypeError):
            continue

        tree = ast.parse(textwrap.dedent(source))
        visitor = FunctionCallCollector()
        visitor.visit(tree)

        for fname in visitor.called_functions:
            if fname in available_functions:
                to_process.append(available_functions[fname])

    return collected


def function_to_tempfile_code(func: FunctionType):
    functions = collect_called_user_functions(func)

    output = ""

    for fn in sorted(functions, key=lambda x: x.__name__):
        try:
            source = textwrap.dedent(inspect.getsource(fn))
            output += f"# Function: {fn.__name__}\n"
            output += source + "\n\n"
        except (OSError, TypeError):
            continue

    return output
