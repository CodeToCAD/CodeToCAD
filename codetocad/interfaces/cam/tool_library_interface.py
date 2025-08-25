"""
Tool library interface for CAM operations.

Manages collections of cutting tools with import/export capabilities
and preset tool definitions.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, TYPE_CHECKING
from pathlib import Path

if TYPE_CHECKING:
    from codetocad.interfaces.cam.tool_interface import ToolInterface, ToolType


class ToolLibraryInterface(ABC):
    """Abstract interface for tool library management."""

    def __init__(self):
        self.name: str = "default_library"
        self.description: str = ""
        self.tools: dict[int, "ToolInterface"] = {}  # tool_number -> tool
        self.categories: dict[str, list[int]] = {}  # category -> tool_numbers
        self.custom_properties: dict[str, Any] = {}

    def set_name(self, name: str) -> "ToolLibraryInterface":
        """Set the library name."""
        self.name = name
        return self

    def set_description(self, description: str) -> "ToolLibraryInterface":
        """Set the library description."""
        self.description = description
        return self

    def add_tool(self, tool: "ToolInterface") -> "ToolLibraryInterface":
        """Add a tool to the library."""
        if tool.tool_number in self.tools:
            raise ValueError(
                f"Tool number {tool.tool_number} already exists in library"
            )

        self.tools[tool.tool_number] = tool

        # Add to category if specified
        category = getattr(tool, "category", None)
        if category:
            if category not in self.categories:
                self.categories[category] = []
            self.categories[category].append(tool.tool_number)

        return self

    def remove_tool(self, tool_number: int) -> "ToolLibraryInterface":
        """Remove a tool from the library."""
        if tool_number not in self.tools:
            raise ValueError(f"Tool number {tool_number} not found in library")

        tool = self.tools[tool_number]
        del self.tools[tool_number]

        # Remove from categories
        for category, tool_numbers in self.categories.items():
            if tool_number in tool_numbers:
                tool_numbers.remove(tool_number)
                if not tool_numbers:  # Remove empty category
                    del self.categories[category]
                break

        return self

    def get_tool(self, tool_number: int) -> "ToolInterface | None":
        """Get a tool by tool number."""
        return self.tools.get(tool_number)

    def get_tools_by_type(self, tool_type: "ToolType") -> list["ToolInterface"]:
        """Get all tools of a specific type."""
        return [tool for tool in self.tools.values() if tool.tool_type == tool_type]

    def get_tools_by_category(self, category: str) -> list["ToolInterface"]:
        """Get all tools in a category."""
        tool_numbers = self.categories.get(category, [])
        return [self.tools[num] for num in tool_numbers if num in self.tools]

    def get_tools_by_diameter_range(
        self, min_diameter: float, max_diameter: float
    ) -> list["ToolInterface"]:
        """Get tools within a diameter range."""
        result = []
        for tool in self.tools.values():
            if tool.geometry and min_diameter <= tool.geometry.diameter <= max_diameter:
                result.append(tool)
        return result

    def get_available_tool_numbers(self) -> list[int]:
        """Get list of all tool numbers in the library."""
        return sorted(self.tools.keys())

    def get_next_available_tool_number(self) -> int:
        """Get the next available tool number."""
        if not self.tools:
            return 1
        return max(self.tools.keys()) + 1

    def find_tools_by_name(self, name_pattern: str) -> list["ToolInterface"]:
        """Find tools by name pattern (case-insensitive)."""
        pattern = name_pattern.lower()
        return [tool for tool in self.tools.values() if pattern in tool.name.lower()]

    def find_tools_by_manufacturer(self, manufacturer: str) -> list["ToolInterface"]:
        """Find tools by manufacturer."""
        manufacturer = manufacturer.lower()
        return [
            tool
            for tool in self.tools.values()
            if manufacturer in tool.manufacturer.lower()
        ]

    def get_library_statistics(self) -> dict[str, Any]:
        """Get statistics about the tool library."""
        stats = {
            "total_tools": len(self.tools),
            "categories": len(self.categories),
            "tool_types": {},
            "diameter_range": {"min": None, "max": None},
            "manufacturers": set(),
        }

        # Count tool types
        for tool in self.tools.values():
            tool_type = tool.tool_type.value
            stats["tool_types"][tool_type] = stats["tool_types"].get(tool_type, 0) + 1

            # Track diameter range
            if tool.geometry:
                diameter = tool.geometry.diameter
                if stats["diameter_range"]["min"] is None:
                    stats["diameter_range"]["min"] = diameter
                    stats["diameter_range"]["max"] = diameter
                else:
                    stats["diameter_range"]["min"] = min(
                        stats["diameter_range"]["min"], diameter
                    )
                    stats["diameter_range"]["max"] = max(
                        stats["diameter_range"]["max"], diameter
                    )

            # Track manufacturers
            if tool.manufacturer:
                stats["manufacturers"].add(tool.manufacturer)

        stats["manufacturers"] = list(stats["manufacturers"])
        return stats

    def validate_library(self) -> list[str]:
        """Validate the tool library and return list of issues."""
        issues = []

        if not self.name:
            issues.append("Library name is required")

        if not self.tools:
            issues.append("Library contains no tools")

        # Check for duplicate tool numbers (shouldn't happen with dict, but safety check)
        tool_numbers = list(self.tools.keys())
        if len(tool_numbers) != len(set(tool_numbers)):
            issues.append("Duplicate tool numbers found")

        # Validate each tool
        for tool_number, tool in self.tools.items():
            if tool.tool_number != tool_number:
                issues.append(
                    f"Tool number mismatch: key={tool_number}, tool.tool_number={tool.tool_number}"
                )

            tool_issues = tool.validate()
            for issue in tool_issues:
                issues.append(f"Tool {tool_number}: {issue}")

        return issues

    def clear(self) -> "ToolLibraryInterface":
        """Clear all tools from the library."""
        self.tools.clear()
        self.categories.clear()
        return self

    def merge_library(
        self, other_library: "ToolLibraryInterface", resolve_conflicts: str = "skip"
    ) -> "ToolLibraryInterface":
        """
        Merge another library into this one.

        Args:
            other_library: Library to merge
            resolve_conflicts: How to handle tool number conflicts
                - "skip": Skip conflicting tools
                - "overwrite": Overwrite existing tools
                - "renumber": Assign new tool numbers to conflicting tools
        """
        for tool_number, tool in other_library.tools.items():
            if tool_number in self.tools:
                if resolve_conflicts == "skip":
                    continue
                elif resolve_conflicts == "overwrite":
                    self.remove_tool(tool_number)
                    self.add_tool(tool.copy())
                elif resolve_conflicts == "renumber":
                    new_tool = tool.copy()
                    new_tool.set_tool_number(self.get_next_available_tool_number())
                    self.add_tool(new_tool)
            else:
                self.add_tool(tool.copy())

        return self

    @abstractmethod
    def save_to_file(self, file_path: str | Path) -> None:
        """Save the tool library to a file."""
        pass

    @abstractmethod
    def load_from_file(self, file_path: str | Path) -> "ToolLibraryInterface":
        """Load the tool library from a file."""
        pass

    @abstractmethod
    def export_to_format(self, file_path: str | Path, format_type: str) -> None:
        """
        Export library to various formats.

        Supported formats might include:
        - "json": JSON format
        - "csv": CSV format for spreadsheet import
        - "xml": XML format
        - "freecad": FreeCAD tool library format
        - "fusion360": Fusion 360 tool library format
        """
        pass

    @abstractmethod
    def import_from_format(
        self, file_path: str | Path, format_type: str
    ) -> "ToolLibraryInterface":
        """Import library from various formats."""
        pass

    def __len__(self) -> int:
        """Return number of tools in library."""
        return len(self.tools)

    def __contains__(self, tool_number: int) -> bool:
        """Check if tool number exists in library."""
        return tool_number in self.tools

    def __iter__(self):
        """Iterate over tools in the library."""
        return iter(self.tools.values())

    def __repr__(self) -> str:
        return f"<ToolLibrary: {self.name}, {len(self.tools)} tools>"
