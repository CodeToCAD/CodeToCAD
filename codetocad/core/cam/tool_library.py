"""
Concrete implementation of Tool Library interface.
"""

import json
import csv
from pathlib import Path
from typing import TYPE_CHECKING

from codetocad.interfaces.cam.tool_library_interface import ToolLibraryInterface

if TYPE_CHECKING:
    pass


class ToolLibrary(ToolLibraryInterface):
    """Concrete implementation of ToolLibraryInterface."""

    def to_json_string(self) -> str:
        """Convert library to string representation."""

        # Create library data structure
        library_data = {
            "name": self.name,
            "description": self.description,
            "tools": {},
            "categories": self.categories,
            "custom_properties": self.custom_properties,
        }

        # Convert tools to dictionary format
        for tool_number, tool in self.tools.items():
            library_data["tools"][str(tool_number)] = tool.to_dict()

        # Write to file
        return json.dumps(library_data, indent=2)

    def save_to_file(self, file_path: str | Path) -> None:
        """Save the tool library to a JSON file."""
        file_path = Path(file_path)

        with open(file_path, "w") as f:
            f.write(self.to_json_string())

    def load_from_file(self, file_path: str | Path) -> "ToolLibrary":
        """Load the tool library from a JSON file."""
        from codetocad.core.cam.tool import Tool

        file_path = Path(file_path)

        with open(file_path, "r") as f:
            library_data = json.load(f)

        # Load basic properties
        self.name = library_data.get("name", "Loaded Library")
        self.description = library_data.get("description", "")
        self.categories = library_data.get("categories", {})
        self.custom_properties = library_data.get("custom_properties", {})

        # Clear existing tools
        self.tools.clear()

        # Load tools
        tools_data = library_data.get("tools", {})
        for tool_number_str, tool_data in tools_data.items():
            tool_number = int(tool_number_str)
            tool = Tool()
            tool.from_dict(tool_data)
            self.tools[tool_number] = tool

        return self

    def export_to_format(self, file_path: str | Path, format_type: str) -> None:
        """Export library to various formats."""
        file_path = Path(file_path)

        if format_type.lower() == "json":
            self.save_to_file(file_path)

        elif format_type.lower() == "csv":
            self._export_to_csv(file_path)

        elif format_type.lower() == "xml":
            self._export_to_xml(file_path)

        else:
            raise ValueError(f"Unsupported export format: {format_type}")

    def import_from_format(
        self, file_path: str | Path, format_type: str
    ) -> "ToolLibrary":
        """Import library from various formats."""
        file_path = Path(file_path)

        if format_type.lower() == "json":
            return self.load_from_file(file_path)

        elif format_type.lower() == "csv":
            return self._import_from_csv(file_path)

        else:
            raise ValueError(f"Unsupported import format: {format_type}")

    def _export_to_csv(self, file_path: Path) -> None:
        """Export tools to CSV format."""
        with open(file_path, "w", newline="") as csvfile:
            fieldnames = [
                "tool_number",
                "name",
                "tool_type",
                "material",
                "diameter",
                "length",
                "cutting_length",
                "flute_count",
                "spindle_speed",
                "feed_rate",
                "manufacturer",
                "description",
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for tool in self.tools.values():
                row = {
                    "tool_number": tool.tool_number,
                    "name": tool.name,
                    "tool_type": tool.tool_type.value,
                    "material": tool.material.value,
                    "diameter": tool.geometry.diameter if tool.geometry else "",
                    "length": tool.geometry.length if tool.geometry else "",
                    "cutting_length": (
                        tool.geometry.cutting_length if tool.geometry else ""
                    ),
                    "flute_count": tool.geometry.flute_count if tool.geometry else "",
                    "spindle_speed": (
                        tool.cutting_data.spindle_speed if tool.cutting_data else ""
                    ),
                    "feed_rate": (
                        tool.cutting_data.feed_rate if tool.cutting_data else ""
                    ),
                    "manufacturer": tool.manufacturer,
                    "description": tool.description,
                }
                writer.writerow(row)

    def _import_from_csv(self, file_path: Path) -> "ToolLibrary":
        """Import tools from CSV format."""
        from codetocad.core.cam.tool import Tool
        from codetocad.interfaces.cam.tool_interface import (
            ToolType,
            ToolMaterial,
            ToolGeometry,
            CuttingData,
        )

        self.tools.clear()

        with open(file_path, "r") as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                tool = Tool()

                # Basic properties
                tool.set_tool_number(int(row["tool_number"]))
                tool.set_name(row["name"])
                tool.tool_type = ToolType(row["tool_type"])
                tool.material = ToolMaterial(row["material"])
                tool.set_manufacturer(row.get("manufacturer", ""))
                tool.set_description(row.get("description", ""))

                # Geometry
                if row.get("diameter"):
                    geometry = ToolGeometry(
                        diameter=float(row["diameter"]),
                        length=float(row.get("length", 50.0)),
                        cutting_length=float(row.get("cutting_length", 20.0)),
                        shank_diameter=float(row.get("diameter", 6.0)),
                        flute_count=int(row.get("flute_count", 2)),
                    )
                    tool.set_geometry(geometry)

                # Cutting data
                if row.get("spindle_speed"):
                    cutting_data = CuttingData(
                        spindle_speed=float(row["spindle_speed"]),
                        feed_rate=float(row.get("feed_rate", 1000.0)),
                        plunge_rate=float(row.get("feed_rate", 1000.0)) * 0.25,
                        step_over=0.5,
                        step_down=1.0,
                    )
                    tool.set_cutting_data(cutting_data)

                self.add_tool(tool)

        return self

    def _export_to_xml(self, file_path: Path) -> None:
        """Export tools to XML format."""
        import xml.etree.ElementTree as ET

        root = ET.Element("ToolLibrary")
        root.set("name", self.name)
        root.set("description", self.description)

        tools_element = ET.SubElement(root, "Tools")

        for tool in self.tools.values():
            tool_element = ET.SubElement(tools_element, "Tool")
            tool_element.set("number", str(tool.tool_number))
            tool_element.set("name", tool.name)
            tool_element.set("type", tool.tool_type.value)
            tool_element.set("material", tool.material.value)

            if tool.geometry:
                geometry_element = ET.SubElement(tool_element, "Geometry")
                geometry_element.set("diameter", str(tool.geometry.diameter))
                geometry_element.set("length", str(tool.geometry.length))
                geometry_element.set(
                    "cutting_length", str(tool.geometry.cutting_length)
                )
                geometry_element.set("flute_count", str(tool.geometry.flute_count))

            if tool.cutting_data:
                cutting_element = ET.SubElement(tool_element, "CuttingData")
                cutting_element.set(
                    "spindle_speed", str(tool.cutting_data.spindle_speed)
                )
                cutting_element.set("feed_rate", str(tool.cutting_data.feed_rate))
                cutting_element.set("plunge_rate", str(tool.cutting_data.plunge_rate))

        tree = ET.ElementTree(root)
        tree.write(file_path, encoding="utf-8", xml_declaration=True)
