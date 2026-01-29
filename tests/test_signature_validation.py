"""
AST-based unit test to validate method signature consistency between core and integration files.

This test ensures that all methods defined in core/cad/*.py files have matching signatures
in their corresponding integration files (e.g., integrations/build123d/cad/*.py).
"""

import ast
import os
from pathlib import Path
from typing import Any


def get_function_signatures(file_path: str) -> dict[str, dict[str, Any]]:
    """
    Extract function signatures from a Python file using AST.

    Only extracts top-level function definitions, not nested functions.

    Args:
        file_path: Path to the Python file to parse

    Returns:
        Dictionary mapping function names to their signature details
    """
    with open(file_path, "r") as f:
        tree = ast.parse(f.read(), filename=file_path)

    signatures = {}

    # Only iterate through top-level nodes in the module body
    # This avoids capturing nested function definitions
    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            # Extract parameter information
            params = []
            defaults_offset = len(node.args.args) - len(node.args.defaults)

            for i, arg in enumerate(node.args.args):
                param_info = {
                    "name": arg.arg,
                    "annotation": (
                        ast.unparse(arg.annotation) if arg.annotation else None
                    ),
                    "default": None,
                }

                # Check if this parameter has a default value
                default_index = i - defaults_offset
                if default_index >= 0:
                    param_info["default"] = ast.unparse(
                        node.args.defaults[default_index]
                    )

                params.append(param_info)

            # Extract return type annotation
            return_annotation = ast.unparse(node.returns) if node.returns else None

            signatures[node.name] = {
                "params": params,
                "return_annotation": return_annotation,
            }

    return signatures


def test_signature_consistency():
    """
    Test that all core method signatures match their integration implementations.

    This test:
    1. Iterates through all /cad folders in codetocad/integrations/*/cad/
    2. For each file found (e.g., draw.py, shape.py), locates the corresponding file in codetocad/core/cad/
    3. Uses AST to extract all function definitions from both files
    4. Verifies that every method defined in the core file exists in the integration file with a matching signature
    """
    # Get the repository root (parent of tests directory)
    repo_root = Path(__file__).parent.parent
    core_cad_dir = repo_root / "codetocad" / "core" / "cad"
    integrations_dir = repo_root / "codetocad" / "integrations"

    # Find all integration directories
    integration_dirs = [
        d for d in integrations_dir.iterdir() if d.is_dir() and (d / "cad").exists()
    ]

    errors = []

    for integration_dir in integration_dirs:
        integration_name = integration_dir.name
        integration_cad_dir = integration_dir / "cad"

        # Find all Python files in the integration's cad directory
        for integration_file in integration_cad_dir.glob("*.py"):
            if integration_file.name.startswith("__"):
                continue  # Skip __init__.py and similar files

            # Find the corresponding core file
            core_file = core_cad_dir / integration_file.name

            if not core_file.exists():
                # Integration file has no corresponding core file - this is okay
                continue

            # Extract signatures from both files
            core_signatures = get_function_signatures(str(core_file))
            integration_signatures = get_function_signatures(str(integration_file))

            # Check each core function
            for func_name, core_sig in core_signatures.items():
                if func_name.startswith("_"):
                    # Skip private functions
                    continue

                # Check if function exists in integration
                if func_name not in integration_signatures:
                    errors.append(
                        f"{integration_name}/{integration_file.name}: Missing function '{func_name}' "
                        f"(defined in core/{integration_file.name})"
                    )
                    continue

                integration_sig = integration_signatures[func_name]

                # Compare parameters
                core_params = core_sig["params"]
                integration_params = integration_sig["params"]

                if len(core_params) != len(integration_params):
                    errors.append(
                        f"{integration_name}/{integration_file.name}::{func_name}: "
                        f"Parameter count mismatch (core: {len(core_params)}, integration: {len(integration_params)})"
                    )
                    continue

                # Check each parameter
                for core_param, integration_param in zip(
                    core_params, integration_params
                ):
                    # Check parameter name
                    if core_param["name"] != integration_param["name"]:
                        errors.append(
                            f"{integration_name}/{integration_file.name}::{func_name}: "
                            f"Parameter name mismatch (core: '{core_param['name']}', integration: '{integration_param['name']}')"
                        )

                    # Check parameter type annotation
                    if core_param["annotation"] != integration_param["annotation"]:
                        errors.append(
                            f"{integration_name}/{integration_file.name}::{func_name}::{core_param['name']}: "
                            f"Type annotation mismatch (core: {core_param['annotation']}, integration: {integration_param['annotation']})"
                        )

                    # Check default value
                    if core_param["default"] != integration_param["default"]:
                        errors.append(
                            f"{integration_name}/{integration_file.name}::{func_name}::{core_param['name']}: "
                            f"Default value mismatch (core: {core_param['default']}, integration: {integration_param['default']})"
                        )

    # Assert no errors were found
    if errors:
        error_message = "\n".join(errors)
        raise AssertionError(f"Signature mismatches found:\n{error_message}")
