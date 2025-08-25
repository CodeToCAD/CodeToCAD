"""
FreeCAD actions for CAM operations.

This module provides low-level FreeCAD operations for CAM functionality
including toolpath generation, tool management, and job setup.
"""

from codetocad.adapters.freecad.freecad_actions.path_operations import (
    create_path_job,
    create_profile_operation,
    create_pocket_operation,
    create_drilling_operation,
    create_adaptive_operation,
    create_surface_operation,
)

from codetocad.adapters.freecad.freecad_actions.tool_operations import (
    create_tool,
    create_tool_controller,
    import_tool_library,
    export_tool_library,
)

from codetocad.adapters.freecad.freecad_actions.job_operations import (
    setup_job_geometry,
    setup_job_stock,
    setup_job_fixtures,
    calculate_toolpaths,
    post_process_job,
)

__all__ = [
    # Path operations
    "create_path_job",
    "create_profile_operation",
    "create_pocket_operation",
    "create_drilling_operation",
    "create_adaptive_operation",
    "create_surface_operation",
    # Tool operations
    "create_tool",
    "create_tool_controller",
    "import_tool_library",
    "export_tool_library",
    # Job operations
    "setup_job_geometry",
    "setup_job_stock",
    "setup_job_fixtures",
    "calculate_toolpaths",
    "post_process_job",
]
