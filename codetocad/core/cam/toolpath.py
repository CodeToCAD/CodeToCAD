"""
Concrete implementation of Toolpath interface.
"""

import copy
from typing import TYPE_CHECKING

from codetocad.interfaces.cam.toolpath_interface import ToolpathInterface

if TYPE_CHECKING:
    from codetocad.interfaces.cad.part.part_interface import PartInterface
    from codetocad.interfaces.cad.sketch.sketch_interface import SketchInterface


class Toolpath(ToolpathInterface):
    """Concrete implementation of ToolpathInterface."""

    def generate_from_sketch(self, sketch: "SketchInterface") -> "Toolpath":
        """Generate toolpath from a 2D sketch."""
        # Basic implementation - would be enhanced by specific adapters
        self.points.clear()

        # This is a placeholder implementation
        # Real implementations would analyze the sketch geometry
        # and generate appropriate toolpath points

        return self

    def generate_from_part(self, part: "PartInterface") -> "Toolpath":
        """Generate toolpath from a 3D part."""
        # Basic implementation - would be enhanced by specific adapters
        self.points.clear()

        # This is a placeholder implementation
        # Real implementations would analyze the part geometry
        # and generate appropriate 3D toolpath points

        return self

    def generate_drilling_pattern(
        self, points: list[tuple[float, float]], depth: float
    ) -> "Toolpath":
        """Generate drilling toolpath from point coordinates."""
        from codetocad.interfaces.cam.toolpath_interface import ToolpathPoint

        self.points.clear()

        if not self.cutting_parameters:
            raise ValueError(
                "Cutting parameters must be set before generating drilling pattern"
            )

        safe_z = self.cutting_parameters.safe_height
        clearance_z = self.cutting_parameters.clearance_height

        # Start at safe height
        if points:
            first_point = points[0]
            self.points.append(
                ToolpathPoint(
                    x=first_point[0], y=first_point[1], z=safe_z, rapid_move=True
                )
            )

        # Generate drilling sequence
        for x, y in points:
            # Rapid to position above hole
            self.points.append(ToolpathPoint(x=x, y=y, z=clearance_z, rapid_move=True))

            # Plunge to depth
            self.points.append(
                ToolpathPoint(
                    x=x, y=y, z=-depth, feed_rate=self.cutting_parameters.plunge_rate
                )
            )

            # Retract to clearance
            self.points.append(ToolpathPoint(x=x, y=y, z=clearance_z, rapid_move=True))

        # Return to safe height
        if points:
            last_point = points[-1]
            self.points.append(
                ToolpathPoint(
                    x=last_point[0], y=last_point[1], z=safe_z, rapid_move=True
                )
            )

        return self

    def optimize_toolpath(self) -> "Toolpath":
        """Optimize the toolpath for efficiency and quality."""
        if not self.points:
            return self

        # Basic optimization: remove duplicate consecutive points
        optimized_points = [self.points[0]]

        for i in range(1, len(self.points)):
            current = self.points[i]
            previous = optimized_points[-1]

            # Skip if same position (within tolerance)
            tolerance = 0.001  # mm
            if (
                abs(current.x - previous.x) > tolerance
                or abs(current.y - previous.y) > tolerance
                or abs(current.z - previous.z) > tolerance
            ):
                optimized_points.append(current)

        self.points = optimized_points
        return self

    def copy(self) -> "Toolpath":
        """Create a copy of the toolpath."""
        new_toolpath = Toolpath()

        # Copy basic properties
        new_toolpath.name = self.name
        new_toolpath.operation = self.operation
        new_toolpath.strategy = self.strategy
        new_toolpath.description = self.description
        new_toolpath.enabled = self.enabled

        # Copy tool reference (shallow copy)
        new_toolpath.tool = self.tool

        # Deep copy cutting parameters and points
        if self.cutting_parameters:
            new_toolpath.cutting_parameters = copy.deepcopy(self.cutting_parameters)

        new_toolpath.points = copy.deepcopy(self.points)
        new_toolpath.custom_properties = copy.deepcopy(self.custom_properties)

        return new_toolpath
