"""
PyCAM toolpath generation operations.

This module provides low-level operations for generating toolpaths
using PyCAM algorithms.
"""

from typing import Tuple, Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


def _ensure_pycam_available():
    """Ensure PyCAM is available and import required modules."""
    try:
        import pycam
        import pycam.Geometry
        import pycam.PathGenerators
        import pycam.Toolpath

        return pycam
    except ImportError as e:
        logger.warning(f"PyCAM not available: {e}")
        # Return None to indicate PyCAM is not available
        return None


def generate_contour_toolpath(
    model: Any, tool_settings: dict[str, Any], operation_settings: dict[str, Any]
) -> list[tuple[float, float, float]]:
    """Generate contour following toolpath using PyCAM."""
    pycam = _ensure_pycam_available()
    if not pycam:
        return _generate_fallback_contour(model, tool_settings, operation_settings)

    try:
        # Extract settings
        tool_radius = tool_settings.get("radius", 3.0)
        step_down = operation_settings.get("step_down", 1.0)
        start_z = operation_settings.get("start_z", 0.0)
        end_z = operation_settings.get("end_z", -5.0)

        # Create tool
        tool = pycam.Geometry.ToolCylindrical(tool_radius)

        # Generate contour toolpath
        path_generator = pycam.PathGenerators.ContourFollow()

        # Configure path generator
        path_generator.set_model(model)
        path_generator.set_tool(tool)

        # Generate toolpath layers
        toolpath_points = []
        current_z = start_z

        while current_z >= end_z:
            # Generate contour at current Z level
            layer_path = path_generator.generate_toolpath(current_z)

            if layer_path:
                # Convert PyCAM path to our format
                for point in layer_path:
                    toolpath_points.append((point.x, point.y, current_z))

            current_z -= step_down

        logger.info(f"Generated contour toolpath: {len(toolpath_points)} points")
        return toolpath_points

    except Exception as e:
        logger.error(f"Failed to generate contour toolpath with PyCAM: {e}")
        return _generate_fallback_contour(model, tool_settings, operation_settings)


def generate_waterline_toolpath(
    model: Any, tool_settings: dict[str, Any], operation_settings: dict[str, Any]
) -> list[tuple[float, float, float]]:
    """Generate waterline toolpath using PyCAM."""
    pycam = _ensure_pycam_available()
    if not pycam:
        return _generate_fallback_waterline(model, tool_settings, operation_settings)

    try:
        # Extract settings
        tool_radius = tool_settings.get("radius", 3.0)
        step_down = operation_settings.get("step_down", 0.5)
        start_z = operation_settings.get("start_z", 0.0)
        end_z = operation_settings.get("end_z", -5.0)

        # Create tool
        tool = pycam.Geometry.ToolCylindrical(tool_radius)

        # Generate waterline toolpath
        path_generator = pycam.PathGenerators.Waterline()

        # Configure path generator
        path_generator.set_model(model)
        path_generator.set_tool(tool)

        # Generate toolpath layers
        toolpath_points = []
        current_z = start_z

        while current_z >= end_z:
            # Generate waterline at current Z level
            layer_paths = path_generator.generate_toolpath(current_z)

            if layer_paths:
                for path in layer_paths:
                    for point in path:
                        toolpath_points.append((point.x, point.y, current_z))

            current_z -= step_down

        logger.info(f"Generated waterline toolpath: {len(toolpath_points)} points")
        return toolpath_points

    except Exception as e:
        logger.error(f"Failed to generate waterline toolpath with PyCAM: {e}")
        return _generate_fallback_waterline(model, tool_settings, operation_settings)


def generate_push_cutter_toolpath(
    model: Any, tool_settings: dict[str, Any], operation_settings: dict[str, Any]
) -> list[tuple[float, float, float]]:
    """Generate push cutter toolpath using PyCAM."""
    pycam = _ensure_pycam_available()
    if not pycam:
        return _generate_fallback_push_cutter(model, tool_settings, operation_settings)

    try:
        # Extract settings
        tool_radius = tool_settings.get("radius", 3.0)
        step_over = operation_settings.get("step_over", 1.0)
        direction = operation_settings.get("direction", "x")  # 'x' or 'y'
        start_z = operation_settings.get("start_z", 0.0)
        end_z = operation_settings.get("end_z", -5.0)

        # Create tool
        tool = pycam.Geometry.ToolCylindrical(tool_radius)

        # Generate push cutter toolpath
        path_generator = pycam.PathGenerators.PushCutter()

        # Configure path generator
        path_generator.set_model(model)
        path_generator.set_tool(tool)
        path_generator.set_direction(direction)
        path_generator.set_step_over(step_over)

        # Generate toolpath
        toolpath = path_generator.generate_toolpath(start_z, end_z)

        # Convert to our format
        toolpath_points = []
        if toolpath:
            for point in toolpath:
                toolpath_points.append((point.x, point.y, point.z))

        logger.info(f"Generated push cutter toolpath: {len(toolpath_points)} points")
        return toolpath_points

    except Exception as e:
        logger.error(f"Failed to generate push cutter toolpath with PyCAM: {e}")
        return _generate_fallback_push_cutter(model, tool_settings, operation_settings)


def generate_drop_cutter_toolpath(
    model: Any, tool_settings: dict[str, Any], operation_settings: dict[str, Any]
) -> list[tuple[float, float, float]]:
    """Generate drop cutter toolpath using PyCAM."""
    pycam = _ensure_pycam_available()
    if not pycam:
        return _generate_fallback_drop_cutter(model, tool_settings, operation_settings)

    try:
        # Extract settings
        tool_radius = tool_settings.get("radius", 3.0)
        step_over = operation_settings.get("step_over", 0.5)
        sample_distance = operation_settings.get("sample_distance", 0.1)

        # Create tool
        if tool_settings.get("type") == "ball":
            tool = pycam.Geometry.ToolSpherical(tool_radius)
        else:
            tool = pycam.Geometry.ToolCylindrical(tool_radius)

        # Generate drop cutter toolpath
        path_generator = pycam.PathGenerators.DropCutter()

        # Configure path generator
        path_generator.set_model(model)
        path_generator.set_tool(tool)
        path_generator.set_step_over(step_over)
        path_generator.set_sample_distance(sample_distance)

        # Generate toolpath
        toolpath = path_generator.generate_toolpath()

        # Convert to our format
        toolpath_points = []
        if toolpath:
            for point in toolpath:
                toolpath_points.append((point.x, point.y, point.z))

        logger.info(f"Generated drop cutter toolpath: {len(toolpath_points)} points")
        return toolpath_points

    except Exception as e:
        logger.error(f"Failed to generate drop cutter toolpath with PyCAM: {e}")
        return _generate_fallback_drop_cutter(model, tool_settings, operation_settings)


# Fallback implementations when PyCAM is not available
def _generate_fallback_contour(
    model: Any, tool_settings: dict[str, Any], operation_settings: dict[str, Any]
) -> list[tuple[float, float, float]]:
    """Generate basic contour toolpath without PyCAM."""
    logger.info("Using fallback contour generation (PyCAM not available)")

    # Basic rectangular contour as fallback
    tool_radius = tool_settings.get("radius", 3.0)
    step_down = operation_settings.get("step_down", 1.0)
    start_z = operation_settings.get("start_z", 0.0)
    end_z = operation_settings.get("end_z", -5.0)

    # Assume model bounds (would need to be extracted from actual model)
    bounds = getattr(
        model, "bounds", {"x_min": -25, "x_max": 25, "y_min": -25, "y_max": 25}
    )

    toolpath_points = []
    current_z = start_z

    while current_z >= end_z:
        # Generate rectangular contour
        x_min = bounds["x_min"] + tool_radius
        x_max = bounds["x_max"] - tool_radius
        y_min = bounds["y_min"] + tool_radius
        y_max = bounds["y_max"] - tool_radius

        # Rectangular path
        contour = [
            (x_min, y_min, current_z),
            (x_max, y_min, current_z),
            (x_max, y_max, current_z),
            (x_min, y_max, current_z),
            (x_min, y_min, current_z),  # Close the loop
        ]

        toolpath_points.extend(contour)
        current_z -= step_down

    return toolpath_points


def _generate_fallback_waterline(
    model: Any, tool_settings: dict[str, Any], operation_settings: dict[str, Any]
) -> list[tuple[float, float, float]]:
    """Generate basic waterline toolpath without PyCAM."""
    logger.info("Using fallback waterline generation (PyCAM not available)")

    # Similar to contour but with multiple passes
    return _generate_fallback_contour(model, tool_settings, operation_settings)


def _generate_fallback_push_cutter(
    model: Any, tool_settings: dict[str, Any], operation_settings: dict[str, Any]
) -> list[tuple[float, float, float]]:
    """Generate basic push cutter toolpath without PyCAM."""
    logger.info("Using fallback push cutter generation (PyCAM not available)")

    tool_radius = tool_settings.get("radius", 3.0)
    step_over = operation_settings.get("step_over", 1.0)
    direction = operation_settings.get("direction", "x")
    start_z = operation_settings.get("start_z", 0.0)
    end_z = operation_settings.get("end_z", -5.0)

    # Assume model bounds
    bounds = getattr(
        model, "bounds", {"x_min": -25, "x_max": 25, "y_min": -25, "y_max": 25}
    )

    toolpath_points = []

    if direction == "x":
        # Cut along X direction
        y = bounds["y_min"] + tool_radius
        while y <= bounds["y_max"] - tool_radius:
            toolpath_points.extend(
                [
                    (bounds["x_min"] + tool_radius, y, start_z),
                    (bounds["x_min"] + tool_radius, y, end_z),
                    (bounds["x_max"] - tool_radius, y, end_z),
                    (bounds["x_max"] - tool_radius, y, start_z),
                ]
            )
            y += step_over
    else:
        # Cut along Y direction
        x = bounds["x_min"] + tool_radius
        while x <= bounds["x_max"] - tool_radius:
            toolpath_points.extend(
                [
                    (x, bounds["y_min"] + tool_radius, start_z),
                    (x, bounds["y_min"] + tool_radius, end_z),
                    (x, bounds["y_max"] - tool_radius, end_z),
                    (x, bounds["y_max"] - tool_radius, start_z),
                ]
            )
            x += step_over

    return toolpath_points


def _generate_fallback_drop_cutter(
    model: Any, tool_settings: dict[str, Any], operation_settings: dict[str, Any]
) -> list[tuple[float, float, float]]:
    """Generate basic drop cutter toolpath without PyCAM."""
    logger.info("Using fallback drop cutter generation (PyCAM not available)")

    # Use push cutter as fallback for drop cutter
    return _generate_fallback_push_cutter(model, tool_settings, operation_settings)


def optimize_toolpath_order(
    toolpath_points: list[tuple[float, float, float]],
) -> list[tuple[float, float, float]]:
    """Optimize toolpath point order to minimize travel time."""
    if len(toolpath_points) < 2:
        return toolpath_points

    try:
        # Simple nearest neighbor optimization
        optimized = [toolpath_points[0]]
        remaining = toolpath_points[1:]

        while remaining:
            current = optimized[-1]

            # Find nearest point
            nearest_idx = 0
            min_distance = float("inf")

            for i, point in enumerate(remaining):
                dx = point[0] - current[0]
                dy = point[1] - current[1]
                dz = point[2] - current[2]
                distance = (dx * dx + dy * dy + dz * dz) ** 0.5

                if distance < min_distance:
                    min_distance = distance
                    nearest_idx = i

            # Add nearest point and remove from remaining
            optimized.append(remaining.pop(nearest_idx))

        logger.info(f"Optimized toolpath order: {len(optimized)} points")
        return optimized

    except Exception as e:
        logger.error(f"Failed to optimize toolpath order: {e}")
        return toolpath_points
