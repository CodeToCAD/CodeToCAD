"""
FreeCAD-specific Tool implementation.
"""

from typing import Dict, Any
import logging

from codetocad.core.cam.tool import Tool as BaseTool
from codetocad.adapters.freecad.freecad_actions.tool_operations import (
    create_tool,
    calculate_feeds_speeds,
    get_tool_shape_file,
)

logger = logging.getLogger(__name__)


class Tool(BaseTool):
    """FreeCAD-specific implementation of ToolInterface."""

    def __init__(self):
        super().__init__()
        self.freecad_tool = None  # Reference to FreeCAD Path.Tool object

    def create_freecad_tool(self) -> Any:
        """Create the underlying FreeCAD Path.Tool object."""
        try:
            if not self.geometry:
                raise ValueError(
                    "Tool geometry must be set before creating FreeCAD tool"
                )

            # Create FreeCAD tool
            self.freecad_tool = create_tool(
                name=self.name,
                tool_type=self.tool_type.value,
                diameter=self.geometry.diameter,
                length=self.geometry.length,
                cutting_edge_height=self.geometry.cutting_length,
                material=self.material.value,
                flute_count=self.geometry.flute_count,
                tip_angle=self.geometry.tip_angle,
                helix_angle=self.geometry.helix_angle,
            )

            # Set additional properties
            if self.description:
                self.freecad_tool.Comment = self.description

            logger.info(f"Created FreeCAD tool: {self.name}")
            return self.freecad_tool

        except Exception as e:
            logger.error(f"Failed to create FreeCAD tool: {e}")
            raise

    def get_freecad_tool(self) -> Any:
        """Get the FreeCAD tool object, creating it if necessary."""
        if self.freecad_tool is None:
            self.create_freecad_tool()
        return self.freecad_tool

    def update_from_freecad_tool(self, freecad_tool) -> "Tool":
        """Update this tool from a FreeCAD Path.Tool object."""
        try:
            from codetocad.interfaces.cam.tool_interface import (
                ToolType,
                ToolMaterial,
                ToolGeometry,
                CuttingData,
            )

            # Update basic properties
            self.name = freecad_tool.Name
            self.description = getattr(freecad_tool, "Comment", "")

            # Map FreeCAD tool type to our enum
            tool_type_map = {
                "EndMill": ToolType.FLAT_END_MILL,
                "BallEndMill": ToolType.BALL_END_MILL,
                "Drill": ToolType.DRILL,
                "VBit": ToolType.V_BIT,
                "ChamferMill": ToolType.CHAMFER_MILL,
            }
            self.tool_type = tool_type_map.get(
                freecad_tool.ToolType, ToolType.FLAT_END_MILL
            )

            # Map material
            material_map = {
                "HighSpeedSteel": ToolMaterial.HSS,
                "Carbide": ToolMaterial.CARBIDE,
                "Ceramic": ToolMaterial.CERAMIC,
                "Diamond": ToolMaterial.DIAMOND,
            }
            self.material = material_map.get(freecad_tool.Material, ToolMaterial.HSS)

            # Update geometry
            self.geometry = ToolGeometry(
                diameter=freecad_tool.Diameter,
                length=freecad_tool.Length,
                cutting_length=getattr(
                    freecad_tool, "CuttingEdgeHeight", freecad_tool.Length * 0.6
                ),
                shank_diameter=freecad_tool.Diameter,  # Assume same as cutting diameter
                flute_count=getattr(freecad_tool, "FluteCount", 2),
                tip_angle=getattr(freecad_tool, "TipAngle", None),
                helix_angle=getattr(freecad_tool, "HelixAngle", None),
            )

            # Store reference to FreeCAD tool
            self.freecad_tool = freecad_tool

            logger.info(f"Updated tool from FreeCAD: {self.name}")
            return self

        except Exception as e:
            logger.error(f"Failed to update from FreeCAD tool: {e}")
            raise

    def calculate_recommended_speeds_feeds(
        self, material: str = "aluminum"
    ) -> dict[str, float]:
        """Calculate recommended speeds and feeds using FreeCAD algorithms."""
        try:
            if not self.freecad_tool:
                self.create_freecad_tool()

            # Use FreeCAD's calculation
            feeds_speeds = calculate_feeds_speeds(self.freecad_tool, material)

            # Update our cutting data if not already set
            if not self.cutting_data:
                from codetocad.interfaces.cam.tool_interface import CuttingData

                self.cutting_data = CuttingData(
                    spindle_speed=feeds_speeds["spindle_speed"],
                    feed_rate=feeds_speeds["feed_rate"],
                    plunge_rate=feeds_speeds["plunge_rate"],
                    step_over=0.5,  # 50% default
                    step_down=self.geometry.diameter * 0.2 if self.geometry else 1.0,
                )

            logger.info(f"Calculated feeds/speeds for {self.name}: {feeds_speeds}")
            return feeds_speeds

        except Exception as e:
            logger.error(f"Failed to calculate feeds/speeds: {e}")
            # Return default values
            return {
                "spindle_speed": 12000.0,
                "feed_rate": 1000.0,
                "plunge_rate": 250.0,
            }

    def get_tool_shape_file(self) -> str | None:
        """Get the FreeCAD tool shape file for this tool type."""
        try:
            return get_tool_shape_file(self.tool_type.value)
        except Exception as e:
            logger.error(f"Failed to get tool shape file: {e}")
            return None

    def validate_for_material(self, material: str) -> list[str]:
        """Validate tool suitability for a specific material."""
        issues = []

        try:
            material_lower = material.lower()

            # Material-specific validation
            if material_lower in ["steel", "stainless_steel", "titanium"]:
                if self.material == self.material.HSS:
                    issues.append("HSS tools may wear quickly on hard materials")
                if self.cutting_data and self.cutting_data.spindle_speed > 8000:
                    issues.append(
                        "High spindle speeds may cause excessive tool wear on hard materials"
                    )

            elif material_lower in ["aluminum", "brass", "copper"]:
                if (
                    self.geometry
                    and self.geometry.helix_angle
                    and self.geometry.helix_angle < 25
                ):
                    issues.append(
                        "Low helix angle may cause chip welding in soft materials"
                    )

            elif material_lower in ["plastic", "acrylic"]:
                if self.cutting_data and self.cutting_data.spindle_speed < 10000:
                    issues.append("Low spindle speeds may cause melting in plastics")

            # Tool type specific validation
            if self.tool_type.value == "drill" and material_lower == "aluminum":
                if (
                    self.geometry
                    and self.geometry.tip_angle
                    and self.geometry.tip_angle != 135
                ):
                    issues.append("135° tip angle recommended for drilling aluminum")

            logger.info(
                f"Material validation for {self.name} on {material}: {len(issues)} issues"
            )

        except Exception as e:
            logger.error(f"Failed to validate tool for material: {e}")
            issues.append(f"Validation error: {e}")

        return issues

    def export_to_freecad_format(self) -> dict[str, Any]:
        """Export tool data in FreeCAD tool library format."""
        try:
            if not self.freecad_tool:
                self.create_freecad_tool()

            # Create FreeCAD tool library entry
            tool_data = {
                "version": 2,
                "name": self.name,
                "shape": self.get_tool_shape_file() or "endmill.fcstd",
                "parameter": {
                    "Diameter": self.geometry.diameter if self.geometry else 6.0,
                    "Length": self.geometry.length if self.geometry else 50.0,
                    "CuttingEdgeHeight": (
                        self.geometry.cutting_length if self.geometry else 20.0
                    ),
                    "ShankDiameter": (
                        self.geometry.shank_diameter if self.geometry else 6.0
                    ),
                    "FluteCount": self.geometry.flute_count if self.geometry else 2,
                },
                "attribute": {
                    "Material": self.material.value,
                    "Manufacturer": self.manufacturer,
                    "PartNumber": self.part_number,
                    "Description": self.description,
                },
            }

            # Add geometry-specific parameters
            if self.geometry:
                if self.geometry.tip_angle:
                    tool_data["parameter"]["TipAngle"] = self.geometry.tip_angle
                if self.geometry.helix_angle:
                    tool_data["parameter"]["HelixAngle"] = self.geometry.helix_angle
                if self.geometry.corner_radius:
                    tool_data["parameter"]["CornerRadius"] = self.geometry.corner_radius

            # Add cutting data as attributes
            if self.cutting_data:
                tool_data["attribute"].update(
                    {
                        "SpindleSpeed": self.cutting_data.spindle_speed,
                        "FeedRate": self.cutting_data.feed_rate,
                        "PlungeRate": self.cutting_data.plunge_rate,
                    }
                )

            logger.info(f"Exported tool to FreeCAD format: {self.name}")
            return tool_data

        except Exception as e:
            logger.error(f"Failed to export tool to FreeCAD format: {e}")
            raise

    def import_from_freecad_format(self, tool_data: dict[str, Any]) -> "Tool":
        """Import tool data from FreeCAD tool library format."""
        try:
            from codetocad.interfaces.cam.tool_interface import (
                ToolType,
                ToolMaterial,
                ToolGeometry,
                CuttingData,
            )

            # Import basic properties
            self.name = tool_data.get("name", "Imported Tool")

            # Import parameters
            params = tool_data.get("parameter", {})
            if params:
                self.geometry = ToolGeometry(
                    diameter=params.get("Diameter", 6.0),
                    length=params.get("Length", 50.0),
                    cutting_length=params.get("CuttingEdgeHeight", 20.0),
                    shank_diameter=params.get("ShankDiameter", 6.0),
                    flute_count=params.get("FluteCount", 2),
                    tip_angle=params.get("TipAngle"),
                    helix_angle=params.get("HelixAngle"),
                    corner_radius=params.get("CornerRadius"),
                )

            # Import attributes
            attributes = tool_data.get("attribute", {})
            if attributes:
                self.description = attributes.get("Description", "")
                self.manufacturer = attributes.get("Manufacturer", "")
                self.part_number = attributes.get("PartNumber", "")

                # Import material
                material_str = attributes.get("Material", "HighSpeedSteel")
                material_map = {
                    "HighSpeedSteel": ToolMaterial.HSS,
                    "Carbide": ToolMaterial.CARBIDE,
                    "Ceramic": ToolMaterial.CERAMIC,
                    "Diamond": ToolMaterial.DIAMOND,
                }
                self.material = material_map.get(material_str, ToolMaterial.HSS)

                # Import cutting data if present
                if any(
                    key in attributes
                    for key in ["SpindleSpeed", "FeedRate", "PlungeRate"]
                ):
                    self.cutting_data = CuttingData(
                        spindle_speed=attributes.get("SpindleSpeed", 12000.0),
                        feed_rate=attributes.get("FeedRate", 1000.0),
                        plunge_rate=attributes.get("PlungeRate", 250.0),
                        step_over=0.5,
                        step_down=1.0,
                    )

            logger.info(f"Imported tool from FreeCAD format: {self.name}")
            return self

        except Exception as e:
            logger.error(f"Failed to import tool from FreeCAD format: {e}")
            raise
