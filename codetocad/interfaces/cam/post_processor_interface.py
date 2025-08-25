"""
Post-processor interface for CAM operations.

Handles G-code generation and export for different CNC machine controllers
and dialects.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Dict, Any, TextIO, TYPE_CHECKING
from pathlib import Path

if TYPE_CHECKING:
    from codetocad.interfaces.cam.toolpath_interface import (
        ToolpathInterface,
        ToolpathPoint,
    )
    from codetocad.interfaces.cam.tool_interface import ToolInterface


class GCodeDialect(Enum):
    """G-code dialects for different CNC controllers."""

    GRBL = "grbl"  # GRBL (Arduino-based)
    LINUXCNC = "linuxcnc"  # LinuxCNC
    MACH3 = "mach3"  # Mach3/Mach4
    FANUC = "fanuc"  # Fanuc controllers
    HAAS = "haas"  # Haas controllers
    SIEMENS = "siemens"  # Siemens controllers
    HEIDENHAIN = "heidenhain"  # Heidenhain controllers
    GENERIC = "generic"  # Generic G-code


class CoordinateMode(Enum):
    """G-code coordinate modes."""

    ABSOLUTE = "absolute"  # G90 - Absolute positioning
    INCREMENTAL = "incremental"  # G91 - Incremental positioning


class UnitsMode(Enum):
    """G-code units modes."""

    MILLIMETERS = "mm"  # G21 - Metric units
    INCHES = "inches"  # G20 - Imperial units


@dataclass
class MachineConfiguration:
    """CNC machine configuration parameters."""

    name: str = "Generic CNC"
    max_spindle_speed: float = 24000.0  # RPM
    max_feed_rate: float = 10000.0  # mm/min
    rapid_feed_rate: float = 15000.0  # mm/min

    # Machine limits
    x_travel: float = 300.0  # mm
    y_travel: float = 200.0  # mm
    z_travel: float = 100.0  # mm

    # Tool changer
    has_tool_changer: bool = False
    max_tool_number: int = 99

    # Spindle configuration
    spindle_direction_clockwise: str = "M03"
    spindle_direction_counterclockwise: str = "M04"
    spindle_stop: str = "M05"

    # Coolant configuration
    coolant_flood: str = "M08"
    coolant_mist: str = "M07"
    coolant_off: str = "M09"

    # Program control
    program_start: str = "%"
    program_end: str = "M30"
    program_stop: str = "M00"
    optional_stop: str = "M01"

    # Custom G-codes
    custom_codes: dict[str, str] = None

    def __post_init__(self):
        """Initialize custom codes if not provided."""
        if self.custom_codes is None:
            self.custom_codes = {}


@dataclass
class PostProcessorSettings:
    """Post-processor configuration settings."""

    dialect: GCodeDialect = GCodeDialect.GENERIC
    coordinate_mode: CoordinateMode = CoordinateMode.ABSOLUTE
    units: UnitsMode = UnitsMode.MILLIMETERS

    # Output formatting
    decimal_places: int = 3
    line_numbers: bool = False
    line_number_increment: int = 10

    # Safety settings
    include_safety_block: bool = True
    safe_z_height: float = 5.0

    # Tool change settings
    include_tool_changes: bool = True
    pause_for_manual_tool_change: bool = False

    # Comments and documentation
    include_comments: bool = True
    include_operation_comments: bool = True
    include_time_estimates: bool = True

    # File settings
    file_extension: str = ".nc"
    header_comment: str = ""
    footer_comment: str = ""


class PostProcessorInterface(ABC):
    """Abstract interface for G-code post-processing."""

    def __init__(self):
        self.name: str = "Generic Post-Processor"
        self.settings: PostProcessorSettings = PostProcessorSettings()
        self.machine_config: MachineConfiguration = MachineConfiguration()
        self.current_position: tuple[float, float, float] | None = None
        self.current_tool: "ToolInterface" | None = None
        self.spindle_running: bool = False
        self.coolant_on: bool = False
        self.line_number: int = 10
        self.custom_properties: dict[str, Any] = {}

    def set_name(self, name: str) -> "PostProcessorInterface":
        """Set the post-processor name."""
        self.name = name
        return self

    def set_settings(self, settings: PostProcessorSettings) -> "PostProcessorInterface":
        """Set post-processor settings."""
        self.settings = settings
        return self

    def set_machine_config(
        self, config: MachineConfiguration
    ) -> "PostProcessorInterface":
        """Set machine configuration."""
        self.machine_config = config
        return self

    def format_coordinate(self, value: float) -> str:
        """Format a coordinate value according to settings."""
        return f"{value:.{self.settings.decimal_places}f}"

    def get_line_number(self) -> str:
        """Get formatted line number if enabled."""
        if not self.settings.line_numbers:
            return ""

        line_num = f"N{self.line_number}"
        self.line_number += self.settings.line_number_increment
        return line_num

    def generate_comment(self, text: str) -> str:
        """Generate a comment line."""
        if not self.settings.include_comments:
            return ""
        return f"({text})"

    def generate_safety_block(self) -> list[str]:
        """Generate safety block at program start."""
        if not self.settings.include_safety_block:
            return []

        lines = []
        lines.append(self.generate_comment("Safety block"))

        # Units
        if self.settings.units == UnitsMode.MILLIMETERS:
            lines.append("G21")  # Metric units
        else:
            lines.append("G20")  # Imperial units

        # Coordinate mode
        if self.settings.coordinate_mode == CoordinateMode.ABSOLUTE:
            lines.append("G90")  # Absolute positioning
        else:
            lines.append("G91")  # Incremental positioning

        # Cancel cutter compensation
        lines.append("G40")  # Cancel cutter radius compensation
        lines.append("G49")  # Cancel tool length compensation

        # Set initial position
        lines.append(f"G00 Z{self.format_coordinate(self.settings.safe_z_height)}")

        return lines

    def generate_tool_change(self, tool: "ToolInterface") -> list[str]:
        """Generate tool change commands."""
        if not self.settings.include_tool_changes:
            return []

        lines = []

        if tool != self.current_tool:
            lines.append(self.generate_comment(f"Tool change: {tool.name}"))

            # Stop spindle and coolant
            lines.append(self.machine_config.spindle_stop)
            lines.append(self.machine_config.coolant_off)

            # Move to safe position
            lines.append(f"G00 Z{self.format_coordinate(self.settings.safe_z_height)}")

            # Tool change
            if self.machine_config.has_tool_changer:
                lines.append(f"T{tool.tool_number}")
                lines.append("M06")  # Tool change
            else:
                lines.append(
                    self.generate_comment(f"Manual tool change to T{tool.tool_number}")
                )
                if self.settings.pause_for_manual_tool_change:
                    lines.append("M00")  # Program stop for manual tool change

            # Tool length compensation
            lines.append(f"G43 H{tool.tool_number}")

            self.current_tool = tool
            self.spindle_running = False
            self.coolant_on = False

        return lines

    def generate_spindle_control(
        self, speed: float, clockwise: bool = True
    ) -> list[str]:
        """Generate spindle control commands."""
        lines = []

        if not self.spindle_running or speed != getattr(
            self, "_current_spindle_speed", 0
        ):
            if clockwise:
                lines.append(
                    f"{self.machine_config.spindle_direction_clockwise} S{int(speed)}"
                )
            else:
                lines.append(
                    f"{self.machine_config.spindle_direction_counterclockwise} S{int(speed)}"
                )

            self.spindle_running = True
            self._current_spindle_speed = speed

        return lines

    def generate_coolant_control(self, enable: bool, flood: bool = True) -> list[str]:
        """Generate coolant control commands."""
        lines = []

        if enable and not self.coolant_on:
            if flood:
                lines.append(self.machine_config.coolant_flood)
            else:
                lines.append(self.machine_config.coolant_mist)
            self.coolant_on = True
        elif not enable and self.coolant_on:
            lines.append(self.machine_config.coolant_off)
            self.coolant_on = False

        return lines

    def generate_movement(self, point: "ToolpathPoint") -> str:
        """Generate movement command for a toolpath point."""
        if point.rapid_move:
            cmd = "G00"
        else:
            cmd = "G01"

        # Build coordinate string
        coords = []
        coords.append(f"X{self.format_coordinate(point.x)}")
        coords.append(f"Y{self.format_coordinate(point.y)}")
        coords.append(f"Z{self.format_coordinate(point.z)}")

        # Add feed rate for cutting moves
        if not point.rapid_move and point.feed_rate:
            coords.append(f"F{self.format_coordinate(point.feed_rate)}")

        line = f"{cmd} {' '.join(coords)}"

        # Add line number if enabled
        line_num = self.get_line_number()
        if line_num:
            line = f"{line_num} {line}"

        self.current_position = (point.x, point.y, point.z)
        return line

    @abstractmethod
    def process_toolpath(self, toolpath: "ToolpathInterface") -> list[str]:
        """Process a toolpath and generate G-code lines."""
        pass

    @abstractmethod
    def process_multiple_toolpaths(
        self, toolpaths: list["ToolpathInterface"]
    ) -> list[str]:
        """Process multiple toolpaths and generate complete G-code program."""
        pass

    @abstractmethod
    def export_to_file(
        self, toolpaths: list["ToolpathInterface"], file_path: str | Path
    ) -> None:
        """Export toolpaths to G-code file."""
        pass

    def validate_toolpaths(self, toolpaths: list["ToolpathInterface"]) -> list[str]:
        """Validate toolpaths for post-processing."""
        issues = []

        for i, toolpath in enumerate(toolpaths):
            if not toolpath.tool:
                issues.append(f"Toolpath {i}: No tool assigned")

            if not toolpath.points:
                issues.append(f"Toolpath {i}: No toolpath points")

            if (
                toolpath.tool
                and toolpath.tool.tool_number > self.machine_config.max_tool_number
            ):
                issues.append(
                    f"Toolpath {i}: Tool number {toolpath.tool.tool_number} exceeds machine limit"
                )

            # Check machine limits
            bounds = toolpath.get_bounding_box()
            if bounds:
                min_point, max_point = bounds
                if max_point[0] > self.machine_config.x_travel:
                    issues.append(f"Toolpath {i}: X travel exceeds machine limit")
                if max_point[1] > self.machine_config.y_travel:
                    issues.append(f"Toolpath {i}: Y travel exceeds machine limit")
                if max_point[2] > self.machine_config.z_travel:
                    issues.append(f"Toolpath {i}: Z travel exceeds machine limit")

        return issues

    def __repr__(self) -> str:
        return f"<PostProcessor: {self.name}, {self.settings.dialect.value}>"
