"""
Concrete implementation of Simulation interface.
"""

from typing import Dict, Any, TYPE_CHECKING
import logging

from codetocad.interfaces.cam.simulation_interface import (
    SimulationInterface,
    CollisionResult,
    MaterialRemovalPreview,
    CollisionType,
)

if TYPE_CHECKING:
    from codetocad.interfaces.cam.toolpath_interface import ToolpathInterface

logger = logging.getLogger(__name__)


class Simulation(SimulationInterface):
    """Concrete implementation of SimulationInterface."""

    def check_collisions(self, toolpath: "ToolpathInterface") -> list[CollisionResult]:
        """Check for collisions in a toolpath."""
        try:
            collisions = []

            if not toolpath.tool or not toolpath.points:
                return collisions

            tool_radius = (
                toolpath.tool.geometry.diameter / 2.0 if toolpath.tool.geometry else 3.0
            )

            # Basic collision checking (simplified implementation)
            for i, point in enumerate(toolpath.points):
                collision_result = self._check_point_collision(point, tool_radius, i)
                if collision_result.has_collision:
                    collisions.append(collision_result)

            logger.info(
                f"Collision check for {toolpath.name}: {len(collisions)} issues found"
            )
            return collisions

        except Exception as e:
            logger.error(f"Failed to check collisions for {toolpath.name}: {e}")
            return []

    def check_multiple_toolpaths(
        self, toolpaths: list["ToolpathInterface"]
    ) -> list[CollisionResult]:
        """Check for collisions across multiple toolpaths."""
        try:
            all_collisions = []

            for toolpath in toolpaths:
                if toolpath.enabled:
                    collisions = self.check_collisions(toolpath)
                    all_collisions.extend(collisions)

            logger.info(
                f"Multi-toolpath collision check: {len(all_collisions)} total issues"
            )
            return all_collisions

        except Exception as e:
            logger.error(f"Failed to check multiple toolpaths: {e}")
            return []

    def simulate_material_removal(
        self, toolpaths: list["ToolpathInterface"]
    ) -> MaterialRemovalPreview:
        """Simulate material removal and generate preview."""
        try:
            # Calculate basic statistics
            total_length = sum(tp.get_total_length() for tp in toolpaths if tp.enabled)
            total_time = sum(
                tp.get_machining_time_estimate() for tp in toolpaths if tp.enabled
            )

            # Estimate volume removed (simplified calculation)
            volume_removed = 0.0
            surface_area = 0.0

            for toolpath in toolpaths:
                if not toolpath.enabled or not toolpath.tool:
                    continue

                tool_diameter = (
                    toolpath.tool.geometry.diameter if toolpath.tool.geometry else 6.0
                )
                path_length = toolpath.get_total_length()

                if toolpath.cutting_parameters:
                    depth = toolpath.cutting_parameters.depth_of_cut
                    step_over = toolpath.cutting_parameters.step_over * tool_diameter

                    # Simplified volume calculation
                    volume_removed += path_length * step_over * depth
                    surface_area += path_length * step_over

            # Estimate surface roughness based on tool and feeds
            roughness_estimate = self._estimate_surface_roughness(toolpaths)

            # Estimate tool wear
            tool_wear_estimate = min(
                total_time / 60.0 * 0.01, 1.0
            )  # 1% wear per hour, max 100%

            preview = MaterialRemovalPreview(
                volume_removed=volume_removed,
                surface_area=surface_area,
                roughness_estimate=roughness_estimate,
                machining_time=total_time,
                tool_wear_estimate=tool_wear_estimate,
                undercuts=[],  # Would need geometric analysis
                thin_walls=[],  # Would need geometric analysis
                sharp_corners=[],  # Would need geometric analysis
            )

            logger.info(
                f"Material removal simulation: {volume_removed:.2f}mm³ removed, "
                f"{total_time:.1f}min machining time"
            )

            return preview

        except Exception as e:
            logger.error(f"Failed to simulate material removal: {e}")
            # Return default preview
            return MaterialRemovalPreview(
                volume_removed=0.0,
                surface_area=0.0,
                roughness_estimate=3.2,
                machining_time=0.0,
                tool_wear_estimate=0.0,
            )

    def verify_toolpath_quality(self, toolpath: "ToolpathInterface") -> dict[str, Any]:
        """Verify toolpath quality and identify potential issues."""
        try:
            quality_report = {
                "overall_quality": "good",
                "issues": [],
                "recommendations": [],
                "statistics": {},
            }

            if not toolpath.points:
                quality_report["overall_quality"] = "poor"
                quality_report["issues"].append("No toolpath points generated")
                return quality_report

            # Analyze toolpath statistics
            total_length = toolpath.get_total_length()
            machining_time = toolpath.get_machining_time_estimate()
            rapid_moves = sum(1 for p in toolpath.points if p.rapid_move)
            cutting_moves = len(toolpath.points) - rapid_moves

            quality_report["statistics"] = {
                "total_points": len(toolpath.points),
                "cutting_moves": cutting_moves,
                "rapid_moves": rapid_moves,
                "total_length": total_length,
                "machining_time": machining_time,
            }

            # Check for quality issues
            if cutting_moves == 0:
                quality_report["issues"].append("No cutting moves found")
                quality_report["overall_quality"] = "poor"

            if total_length < 1.0:
                quality_report["issues"].append("Very short toolpath")
                quality_report["overall_quality"] = "fair"

            # Check for excessive rapid moves
            if rapid_moves > cutting_moves:
                quality_report["issues"].append("More rapid moves than cutting moves")
                quality_report["recommendations"].append("Review toolpath strategy")

            # Check feed rates
            if toolpath.cutting_parameters:
                feed_rate = toolpath.cutting_parameters.feed_rate
                if feed_rate > 5000:
                    quality_report["recommendations"].append(
                        "High feed rate - verify machine capability"
                    )
                elif feed_rate < 100:
                    quality_report["recommendations"].append(
                        "Low feed rate - consider increasing for efficiency"
                    )

            logger.info(
                f"Quality verification for {toolpath.name}: {quality_report['overall_quality']}"
            )
            return quality_report

        except Exception as e:
            logger.error(f"Failed to verify toolpath quality: {e}")
            return {
                "overall_quality": "unknown",
                "issues": [f"Verification failed: {e}"],
                "recommendations": [],
                "statistics": {},
            }

    def _check_point_collision(
        self, point, tool_radius: float, point_index: int
    ) -> CollisionResult:
        """Check for collision at a specific point."""
        # Simplified collision checking
        collision = CollisionResult(has_collision=False)

        # Check if tool goes below workpiece (simplified check)
        if point.z < -50.0:  # Assume workpiece is max 50mm thick
            collision.has_collision = True
            collision.collision_type = CollisionType.TOOL_WORKPIECE
            collision.collision_point = (point.x, point.y, point.z)
            collision.point_index = point_index
            collision.severity = "high"
            collision.description = "Tool extends below workpiece"
            collision.suggested_fix = (
                "Reduce cutting depth or check workpiece thickness"
            )

        # Check for rapid moves at low Z (potential crash)
        if point.rapid_move and point.z < 0:
            collision.has_collision = True
            collision.collision_type = CollisionType.RAPID_MOVE
            collision.collision_point = (point.x, point.y, point.z)
            collision.point_index = point_index
            collision.severity = "critical"
            collision.description = "Rapid move below workpiece surface"
            collision.suggested_fix = "Increase clearance height for rapid moves"

        return collision

    def _estimate_surface_roughness(
        self, toolpaths: list["ToolpathInterface"]
    ) -> float:
        """Estimate surface roughness based on toolpaths."""
        try:
            # Find finishing operations
            finishing_toolpaths = [
                tp
                for tp in toolpaths
                if tp.operation.value == "FINISHING" and tp.enabled
            ]

            if not finishing_toolpaths:
                return 6.3  # Default roughness without finishing

            # Estimate based on tool and parameters
            best_roughness = 6.3

            for toolpath in finishing_toolpaths:
                if not toolpath.tool or not toolpath.cutting_parameters:
                    continue

                tool_diameter = (
                    toolpath.tool.geometry.diameter if toolpath.tool.geometry else 6.0
                )
                step_over = toolpath.cutting_parameters.step_over * tool_diameter
                feed_rate = toolpath.cutting_parameters.feed_rate
                spindle_speed = toolpath.cutting_parameters.spindle_speed

                # Simplified roughness calculation
                # Ra ≈ (feed_per_tooth)² / (8 * tool_radius)
                flute_count = (
                    toolpath.tool.geometry.flute_count if toolpath.tool.geometry else 2
                )
                feed_per_tooth = feed_rate / (spindle_speed * flute_count)
                tool_radius = tool_diameter / 2.0

                estimated_ra = (
                    (feed_per_tooth**2) / (8 * tool_radius) * 1000
                )  # Convert to μm

                # Factor in step over effect
                if step_over > tool_diameter * 0.1:  # More than 10% stepover
                    estimated_ra *= step_over / (tool_diameter * 0.1)

                best_roughness = min(best_roughness, max(0.8, estimated_ra))

            return best_roughness

        except Exception as e:
            logger.error(f"Failed to estimate surface roughness: {e}")
            return 3.2  # Default Ra value
