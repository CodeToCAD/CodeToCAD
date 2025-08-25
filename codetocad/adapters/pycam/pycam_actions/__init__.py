"""
PyCAM actions for CAM operations.

This module provides low-level PyCAM operations for basic CAM functionality
including toolpath generation and G-code export.
"""

from codetocad.adapters.pycam.pycam_actions.toolpath_generation import (
    generate_contour_toolpath,
    generate_waterline_toolpath,
    generate_push_cutter_toolpath,
    generate_drop_cutter_toolpath,
)

from codetocad.adapters.pycam.pycam_actions.model_operations import (
    load_stl_model,
    create_model_from_geometry,
    get_model_bounds,
    validate_model,
)

from codetocad.adapters.pycam.pycam_actions.gcode_export import (
    export_toolpath_to_gcode,
    configure_gcode_settings,
    validate_gcode_output,
)

__all__ = [
    # Toolpath generation
    "generate_contour_toolpath",
    "generate_waterline_toolpath",
    "generate_push_cutter_toolpath",
    "generate_drop_cutter_toolpath",
    # Model operations
    "load_stl_model",
    "create_model_from_geometry",
    "get_model_bounds",
    "validate_model",
    # G-code export
    "export_toolpath_to_gcode",
    "configure_gcode_settings",
    "validate_gcode_output",
]
