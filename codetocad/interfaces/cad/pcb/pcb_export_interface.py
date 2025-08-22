"""
PCB Export interface for CodeToCAD.

This module defines the abstract interface for PCB export operations including
Gerber files, drill files, and other manufacturing outputs.
"""

from abc import ABC, abstractmethod
from typing import Optional
from enum import Enum
from dataclasses import dataclass
from pathlib import Path


class ExportFormat(Enum):
    """Enumeration of export formats."""

    GERBER = "gerber"  # Gerber files
    EXCELLON = "excellon"  # Excellon drill files
    PDF = "pdf"  # PDF documentation
    SVG = "svg"  # SVG graphics
    DXF = "dxf"  # DXF CAD format
    STEP = "step"  # 3D STEP model
    VRML = "vrml"  # 3D VRML model
    PICK_PLACE = "pick_place"  # Pick and place file
    BOM = "bom"  # Bill of materials
    NETLIST = "netlist"  # Netlist file
    POSITION = "position"  # Component position file


@dataclass
class GerberOptions:
    """Options for Gerber export."""

    format_precision: tuple[int, int] = (4, 6)  # (integer, decimal) digits
    units: str = "mm"  # "mm" or "inch"
    zero_suppression: str = "leading"  # "leading", "trailing", "none"
    coordinate_format: str = "absolute"  # "absolute" or "incremental"
    include_aperture_macros: bool = True
    subtract_soldermask: bool = True
    use_drill_file_origin: bool = True
    minimal_header: bool = False


@dataclass
class DrillOptions:
    """Options for drill file export."""

    format_precision: tuple[int, int] = (3, 3)  # (integer, decimal) digits
    units: str = "mm"  # "mm" or "inch"
    zero_suppression: str = "leading"  # "leading", "trailing", "none"
    coordinate_format: str = "absolute"  # "absolute" or "incremental"
    merge_pth_npth: bool = False  # Merge plated and non-plated holes
    generate_map: bool = True  # Generate drill map
    minimal_header: bool = False


@dataclass
class ExportOptions:
    """General export options."""

    output_directory: str = "./pcb_output"
    file_prefix: str = ""
    include_timestamp: bool = True
    overwrite_existing: bool = True
    create_zip_archive: bool = False
    zip_filename: str = "pcb_manufacturing_files.zip"


class PCBExportInterface(ABC):
    """
    Abstract interface for PCB export operations.

    This interface handles exporting PCB designs to various formats
    for manufacturing, documentation, and 3D visualization.
    """

    def __init__(self):
        self.export_options: ExportOptions = ExportOptions()
        self.gerber_options: GerberOptions = GerberOptions()
        self.drill_options: DrillOptions = DrillOptions()

    @abstractmethod
    def export_gerbers(
        self, output_path: str, layer_names: Optional[list[str]] = None
    ) -> list[str]:
        """
        Export Gerber files for manufacturing.

        Args:
            output_path: Output directory path
            layer_names: List of layer names to export (None for all)

        Returns:
            list[str]: List of generated file paths
        """
        ...

    @abstractmethod
    def export_drill_files(self, output_path: str) -> list[str]:
        """
        Export drill files (Excellon format).

        Args:
            output_path: Output directory path

        Returns:
            list[str]: List of generated drill file paths
        """
        ...

    @abstractmethod
    def export_pick_and_place(self, output_path: str, format_type: str = "csv") -> str:
        """
        Export pick and place file for assembly.

        Args:
            output_path: Output file path
            format_type: Format type ("csv", "txt")

        Returns:
            str: Generated file path
        """
        ...

    @abstractmethod
    def export_bill_of_materials(
        self, output_path: str, format_type: str = "csv", include_dnp: bool = False
    ) -> str:
        """
        Export bill of materials.

        Args:
            output_path: Output file path
            format_type: Format type ("csv", "xlsx", "xml")
            include_dnp: Include "Do Not Populate" components

        Returns:
            str: Generated file path
        """
        ...

    @abstractmethod
    def export_3d_model(
        self,
        output_path: str,
        format_type: ExportFormat = ExportFormat.STEP,
        include_components: bool = True,
    ) -> str:
        """
        Export 3D model of the PCB.

        Args:
            output_path: Output file path
            format_type: 3D format (STEP, VRML)
            include_components: Include component 3D models

        Returns:
            str: Generated file path
        """
        ...

    @abstractmethod
    def export_pdf_documentation(
        self,
        output_path: str,
        include_layers: Optional[list[str]] = None,
        include_drill_map: bool = True,
    ) -> str:
        """
        Export PDF documentation.

        Args:
            output_path: Output file path
            include_layers: Layers to include (None for all visible)
            include_drill_map: Include drill map

        Returns:
            str: Generated file path
        """
        ...

    @abstractmethod
    def export_netlist(self, output_path: str, format_type: str = "kicad") -> str:
        """
        Export netlist file.

        Args:
            output_path: Output file path
            format_type: Format type ("kicad", "spice", "generic")

        Returns:
            str: Generated file path
        """
        ...

    @abstractmethod
    def set_gerber_options(self, options: GerberOptions) -> "PCBExportInterface":
        """
        Set Gerber export options.

        Args:
            options: Gerber export options

        Returns:
            PCBExportInterface: Self for method chaining
        """
        ...

    @abstractmethod
    def set_drill_options(self, options: DrillOptions) -> "PCBExportInterface":
        """
        Set drill file export options.

        Args:
            options: Drill export options

        Returns:
            PCBExportInterface: Self for method chaining
        """
        ...

    @abstractmethod
    def create_manufacturing_package(
        self, output_path: str, include_3d: bool = False
    ) -> str:
        """
        Create complete manufacturing package.

        Args:
            output_path: Output directory path
            include_3d: Include 3D models

        Returns:
            str: Path to created package (zip file or directory)
        """
        ...

    @abstractmethod
    def validate_for_manufacturing(self) -> list[str]:
        """
        Validate PCB design for manufacturing.

        Returns:
            list[str]: List of manufacturing issues (empty if valid)
        """
        ...
