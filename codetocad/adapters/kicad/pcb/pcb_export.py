"""
KiCad PCB Export implementation for CodeToCAD.

This module provides KiCad-specific implementation of PCB export operations.
"""

from typing import TYPE_CHECKING
from pathlib import Path
from codetocad.interfaces.cad.pcb.pcb_export_interface import (
    PCBExportInterface,
    ExportFormat,
    GerberOptions,
    DrillOptions,
)


try:
    from kipy import KiCad

    KIPY_AVAILABLE = True
except ImportError:
    try:
        from kicad import KiCad

        KIPY_AVAILABLE = True
    except ImportError:
        KiCad = None
        KIPY_AVAILABLE = False

if TYPE_CHECKING:
    from .pcb_board import PCBBoard


class PCBExport(PCBExportInterface):
    """
    KiCad-specific implementation of PCB export operations.

    This class provides KiCad-specific implementations for exporting
    manufacturing files using KiCad's export capabilities.
    """

    def __init__(self, board: "PCBBoard" | None = None):
        super().__init__()
        self._board = board

    def export_gerbers(
        self, output_path: str, layer_names: list[str] | None = None
    ) -> list[str]:
        """Export Gerber files for manufacturing."""

        try:
            if self._board is None:
                raise RuntimeError("No board associated with exporter")

            from ..kicad_actions.export_operations import export_gerbers

            generated_files = export_gerbers(
                self._board.kicad_board, output_path, layer_names
            )

            return generated_files

        except Exception as e:
            raise RuntimeError(f"Failed to export Gerbers: {str(e)}")

    def export_drill_files(self, output_path: str) -> list[str]:
        """Export drill files (Excellon format)."""

        try:
            if self._board is None:
                raise RuntimeError("No board associated with exporter")

            from ..kicad_actions.export_operations import export_drill_files

            generated_files = export_drill_files(self._board.kicad_board, output_path)

            return generated_files

        except Exception as e:
            raise RuntimeError(f"Failed to export drill files: {str(e)}")

    def export_pick_and_place(self, output_path: str, format_type: str = "csv") -> str:
        """Export pick and place file for assembly."""

        try:
            if self._board is None:
                raise RuntimeError("No board associated with exporter")

            from ..kicad_actions.export_operations import export_pick_and_place

            generated_file = export_pick_and_place(
                self._board.kicad_board, output_path, format_type
            )

            return generated_file

        except Exception as e:
            raise RuntimeError(f"Failed to export pick and place: {str(e)}")

    def export_bill_of_materials(
        self, output_path: str, format_type: str = "csv", include_dnp: bool = False
    ) -> str:
        """Export bill of materials."""
        try:
            if self._board is None:
                raise RuntimeError("No board associated with exporter")

            # Generate BOM from board components
            components = []
            # Note: This is a placeholder implementation
            # The actual implementation would use kipy/kicad-python API
            # to extract component information from the board

            # Placeholder component data
            components = [
                {
                    "reference": "R1",
                    "value": "10k",
                    "footprint": "Resistor_SMD:R_0603_1608Metric",
                    "description": "Resistor",
                    "keywords": "resistor",
                }
            ]

            # Write BOM file
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)

            if format_type.lower() == "csv":
                import csv

                with open(output_path, "w", newline="") as f:
                    if components:
                        writer = csv.DictWriter(f, fieldnames=components[0].keys())
                        writer.writeheader()
                        writer.writerows(components)
            else:
                raise ValueError(f"Unsupported BOM format: {format_type}")

            return output_path

        except Exception as e:
            raise RuntimeError(f"Failed to export BOM: {str(e)}")

    def export_3d_model(
        self,
        output_path: str,
        format_type: ExportFormat = ExportFormat.STEP,
        include_components: bool = True,
    ) -> str:
        """Export 3D model of the PCB."""

        try:
            if self._board is None:
                raise RuntimeError("No board associated with exporter")

            from ..kicad_actions.export_operations import export_3d_model

            generated_file = export_3d_model(
                self._board.kicad_board, output_path, format_type.value
            )

            return generated_file

        except Exception as e:
            raise RuntimeError(f"Failed to export 3D model: {str(e)}")

    def export_pdf_documentation(
        self,
        output_path: str,
        include_layers: list[str] | None = None,
        include_drill_map: bool = True,
    ) -> str:
        """Export PDF documentation."""
        # PDF export would use KiCad's plot controller
        # This is a simplified placeholder implementation
        try:
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)

            # Create a simple text file as placeholder
            with open(output_path, "w") as f:
                f.write("PCB Documentation\n")
                f.write("=================\n\n")
                if self._board:
                    info = self._board.get_info()
                    f.write(f"Board: {info.get('name', 'Unknown')}\n")
                    f.write(f"Components: {info.get('component_count', 0)}\n")
                    f.write(f"Nets: {info.get('net_count', 0)}\n")

            return output_path

        except Exception as e:
            raise RuntimeError(f"Failed to export PDF documentation: {str(e)}")

    def export_netlist(self, output_path: str, format_type: str = "kicad") -> str:
        """Export netlist file."""

        try:
            if self._board is None:
                raise RuntimeError("No board associated with exporter")

            from ..kicad_actions.export_operations import export_netlist

            generated_file = export_netlist(
                self._board.kicad_board, output_path, format_type
            )

            return generated_file

        except Exception as e:
            raise RuntimeError(f"Failed to export netlist: {str(e)}")

    def set_gerber_options(self, options: GerberOptions) -> "PCBExportInterface":
        """Set Gerber export options."""
        self.gerber_options = options
        return self

    def set_drill_options(self, options: DrillOptions) -> "PCBExportInterface":
        """Set drill file export options."""
        self.drill_options = options
        return self

    def create_manufacturing_package(
        self, output_path: str, include_3d: bool = False
    ) -> str:
        """Create complete manufacturing package."""
        try:
            # Create output directory
            Path(output_path).mkdir(parents=True, exist_ok=True)

            generated_files = []

            # Export Gerbers
            gerber_dir = Path(output_path) / "gerbers"
            gerber_files = self.export_gerbers(str(gerber_dir))
            generated_files.extend(gerber_files)

            # Export drill files
            drill_dir = Path(output_path) / "drill"
            drill_files = self.export_drill_files(str(drill_dir))
            generated_files.extend(drill_files)

            # Export pick and place
            pnp_file = self.export_pick_and_place(
                str(Path(output_path) / "assembly.csv")
            )
            generated_files.append(pnp_file)

            # Export BOM
            bom_file = self.export_bill_of_materials(str(Path(output_path) / "bom.csv"))
            generated_files.append(bom_file)

            # Export 3D model if requested
            if include_3d:
                model_file = self.export_3d_model(str(Path(output_path) / "pcb.step"))
                generated_files.append(model_file)

            # Create zip archive if requested
            if self.export_options.create_zip_archive:
                import zipfile

                zip_path = Path(output_path) / self.export_options.zip_filename

                with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
                    for file_path in generated_files:
                        if Path(file_path).exists():
                            arcname = Path(file_path).relative_to(output_path)
                            zipf.write(file_path, arcname)

                return str(zip_path)

            return output_path

        except Exception as e:
            raise RuntimeError(f"Failed to create manufacturing package: {str(e)}")

    def validate_for_manufacturing(self) -> list[str]:
        """Validate PCB design for manufacturing."""
        issues = []

        if self._board is None:
            issues.append("No board associated with exporter")
            return issues

        # Basic manufacturing validation
        try:
            board_info = self._board.get_info()

            if board_info.get("component_count", 0) == 0:
                issues.append("Board has no components")

            if board_info.get("net_count", 0) == 0:
                issues.append("Board has no nets")

            # Check design rules
            drc_violations = self._board.validate_design_rules()
            issues.extend(drc_violations)

        except Exception as e:
            issues.append(f"Validation error: {str(e)}")

        return issues

    def set_board(self, board: "PCBBoard") -> None:
        """Set the parent board (internal method)."""
        self._board = board
