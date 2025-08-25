"""
Concrete implementation of Post Processor interface.
"""

from typing import TextIO, TYPE_CHECKING
from pathlib import Path
import logging

from codetocad.interfaces.cam.post_processor_interface import PostProcessorInterface

if TYPE_CHECKING:
    from codetocad.interfaces.cam.toolpath_interface import ToolpathInterface

logger = logging.getLogger(__name__)


class PostProcessor(PostProcessorInterface):
    """Concrete implementation of PostProcessorInterface."""

    def process_toolpath(self, toolpath: "ToolpathInterface") -> list[str]:
        """Process a toolpath and generate G-code lines."""
        try:
            lines = []

            # Add operation header
            if self.settings.include_operation_comments:
                lines.append(self.generate_comment(f"Operation: {toolpath.name}"))
                lines.append(
                    self.generate_comment(
                        f"Tool: {toolpath.tool.name if toolpath.tool else 'Unknown'}"
                    )
                )
                lines.append(
                    self.generate_comment(f"Strategy: {toolpath.strategy.value}")
                )

            # Tool change if needed
            if toolpath.tool:
                tool_change_lines = self.generate_tool_change(toolpath.tool)
                lines.extend(tool_change_lines)

                # Spindle and coolant control
                if toolpath.tool.cutting_data:
                    spindle_lines = self.generate_spindle_control(
                        toolpath.tool.cutting_data.spindle_speed
                    )
                    lines.extend(spindle_lines)

                    coolant_lines = self.generate_coolant_control(
                        toolpath.tool.cutting_data.coolant
                    )
                    lines.extend(coolant_lines)

            # Process toolpath points
            for point in toolpath.points:
                line = self.generate_movement(point)
                lines.append(line)

            # Add operation footer
            if self.settings.include_operation_comments:
                lines.append(self.generate_comment(f"End operation: {toolpath.name}"))

            logger.info(
                f"Processed toolpath {toolpath.name}: {len(lines)} G-code lines"
            )
            return lines

        except Exception as e:
            logger.error(f"Failed to process toolpath {toolpath.name}: {e}")
            raise

    def process_multiple_toolpaths(
        self, toolpaths: list["ToolpathInterface"]
    ) -> list[str]:
        """Process multiple toolpaths and generate complete G-code program."""
        try:
            lines = []

            # Program header
            if self.settings.program_start:
                lines.append(self.machine_config.program_start)

            if self.settings.include_comments and self.settings.header_comment:
                lines.append(self.generate_comment(self.settings.header_comment))

            # Safety block
            safety_lines = self.generate_safety_block()
            lines.extend(safety_lines)

            # Validate toolpaths
            validation_issues = self.validate_toolpaths(toolpaths)
            if validation_issues:
                for issue in validation_issues:
                    lines.append(self.generate_comment(f"WARNING: {issue}"))

            # Process each toolpath
            for toolpath in toolpaths:
                if toolpath.enabled:
                    toolpath_lines = self.process_toolpath(toolpath)
                    lines.extend(toolpath_lines)
                    lines.append("")  # Empty line between operations

            # Program footer
            lines.append(self.generate_comment("End of program"))
            lines.append(self.machine_config.spindle_stop)
            lines.append(self.machine_config.coolant_off)
            lines.append(f"G00 Z{self.format_coordinate(self.settings.safe_z_height)}")
            lines.append(self.machine_config.program_end)

            if self.settings.include_comments and self.settings.footer_comment:
                lines.append(self.generate_comment(self.settings.footer_comment))

            logger.info(f"Generated complete G-code program: {len(lines)} lines")
            return lines

        except Exception as e:
            logger.error(f"Failed to process multiple toolpaths: {e}")
            raise

    def export_to_file(
        self, toolpaths: list["ToolpathInterface"], file_path: str | Path
    ) -> None:
        """Export toolpaths to G-code file."""
        try:
            file_path = Path(file_path)

            # Generate G-code
            gcode_lines = self.process_multiple_toolpaths(toolpaths)

            # Write to file
            with open(file_path, "w") as f:
                for line in gcode_lines:
                    if line.strip():  # Skip empty lines
                        f.write(line + "\n")

            logger.info(f"Exported G-code to: {file_path}")

        except Exception as e:
            logger.error(f"Failed to export G-code to {file_path}: {e}")
            raise
