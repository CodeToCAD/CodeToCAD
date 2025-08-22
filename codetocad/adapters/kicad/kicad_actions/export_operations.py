"""
KiCad export operations for CodeToCAD.

This module provides low-level KiCad export operations for manufacturing files using kipy.
"""

from pathlib import Path
import os


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


def export_gerbers(
    board, output_dir: str, layer_names: list[str] | None = None
) -> list[str]:
    """
    Export Gerber files.

    Args:
        board: KiCad board object
        output_dir: Output directory path
        layer_names: List of layer names to export (None for all)

    Returns:
        List[str]: List of generated file paths

    Raises:
        RuntimeError: If operation fails
    """

    try:
        # Create output directory
        Path(output_dir).mkdir(parents=True, exist_ok=True)

        # Initialize plot controller
        plot_controller = pcbnew.PLOT_CONTROLLER(board)
        plot_options = plot_controller.GetPlotOptions()

        # Set plot options
        plot_options.SetOutputDirectory(output_dir)
        plot_options.SetPlotFrameRef(False)
        plot_options.SetPlotValue(True)
        plot_options.SetPlotReference(True)
        plot_options.SetPlotInvisibleText(False)
        plot_options.SetPlotViaOnMaskLayer(False)
        plot_options.SetExcludeEdgeLayer(True)
        plot_options.SetFormat(pcbnew.PLOT_FORMAT_GERBER)
        plot_options.SetUseGerberProtelExtensions(True)
        plot_options.SetCreateGerberJobFile(True)
        plot_options.SetSubtractMaskFromSilk(False)
        plot_options.SetGerberPrecision(6)

        # Default layers to export if none specified
        if layer_names is None:
            layer_names = [
                "F.Cu",
                "B.Cu",  # Copper layers
                "F.Paste",
                "B.Paste",  # Paste layers
                "F.SilkS",
                "B.SilkS",  # Silkscreen layers
                "F.Mask",
                "B.Mask",  # Soldermask layers
                "Edge.Cuts",  # Board outline
            ]

        generated_files = []

        # Export each layer
        for layer_name in layer_names:
            layer_id = board.GetLayerID(layer_name)
            if layer_id == pcbnew.UNDEFINED_LAYER:
                continue  # Skip undefined layers

            # Set current layer
            plot_controller.SetLayer(layer_id)
            plot_controller.OpenPlotfile(
                layer_name, pcbnew.PLOT_FORMAT_GERBER, layer_name
            )

            if plot_controller.PlotLayer():
                output_filename = plot_controller.GetPlotFileName()
                generated_files.append(output_filename)

            plot_controller.ClosePlot()

        return generated_files

    except Exception as e:
        raise RuntimeError(f"Failed to export Gerbers: {str(e)}")


def export_drill_files(board: "pcbnew.BOARD", output_dir: str) -> List[str]:
    """
    Export drill files (Excellon format).

    Args:
        board: KiCad board object
        output_dir: Output directory path

    Returns:
        List[str]: List of generated drill file paths

    Raises:
        RuntimeError: If operation fails
    """

    try:
        # Create output directory
        Path(output_dir).mkdir(parents=True, exist_ok=True)

        # Initialize drill writer
        drill_writer = pcbnew.EXCELLON_WRITER(board)
        drill_writer.SetMapFileFormat(pcbnew.PLOT_FORMAT_PDF)

        # Set drill options
        mirror = False
        minimal_header = False
        offset = pcbnew.VECTOR2I(0, 0)
        merge_pth_npth = False

        # Generate drill files
        drill_writer.CreateDrillandMapFilesSet(
            output_dir,
            True,  # Generate drill file
            True,  # Generate map file
            merge_pth_npth,
            minimal_header,
        )

        # Get generated file names
        generated_files = []
        board_name = os.path.splitext(os.path.basename(board.GetFileName()))[0]

        # Standard drill file names
        drill_files = [
            f"{board_name}.drl",  # Drill file
            f"{board_name}-drl_map.pdf",  # Drill map
        ]

        for filename in drill_files:
            filepath = os.path.join(output_dir, filename)
            if os.path.exists(filepath):
                generated_files.append(filepath)

        return generated_files

    except Exception as e:
        raise RuntimeError(f"Failed to export drill files: {str(e)}")


def export_3d_model(
    board: "pcbnew.BOARD", output_path: str, format_type: str = "step"
) -> str:
    """
    Export 3D model of the PCB.

    Args:
        board: KiCad board object
        output_path: Output file path
        format_type: Format type ("step", "vrml")

    Returns:
        str: Generated file path

    Raises:
        RuntimeError: If operation fails
    """

    try:
        # Create output directory
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)

        if format_type.lower() == "step":
            # Export STEP file
            exporter = pcbnew.STEP_PCB_MODEL(board)

            # Set export options
            exporter.SetPCBFileName(board.GetFileName())
            exporter.SetOutputFile(output_path)
            exporter.SetOverwrite(True)
            exporter.SetIncludeUnspecified(True)
            exporter.SetIncludeDNP(False)

            # Perform export
            if not exporter.DoExport():
                raise RuntimeError("STEP export failed")

        elif format_type.lower() == "vrml":
            # Export VRML file
            exporter = pcbnew.VRML_LAYER_EXPORTER(board)
            exporter.ExportVRML_File(output_path, 1.0, True, True)

        else:
            raise ValueError(f"Unsupported 3D format: {format_type}")

        return output_path

    except Exception as e:
        raise RuntimeError(f"Failed to export 3D model: {str(e)}")


def export_netlist(
    board: "pcbnew.BOARD", output_path: str, format_type: str = "kicad"
) -> str:
    """
    Export netlist file.

    Args:
        board: KiCad board object
        output_path: Output file path
        format_type: Format type ("kicad", "spice", "generic")

    Returns:
        str: Generated file path

    Raises:
        RuntimeError: If operation fails
    """

    try:
        # Create output directory
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)

        # Generate netlist content
        netlist_content = []

        if format_type.lower() == "kicad":
            # KiCad netlist format
            netlist_content.append("(export (version D)")
            netlist_content.append("  (design")
            netlist_content.append(f'    (source "{board.GetFileName()}")')
            netlist_content.append("  )")

            # Components
            netlist_content.append("  (components")
            for footprint in board.GetFootprints():
                ref = footprint.GetReference()
                value = footprint.GetValue()
                footprint_name = str(footprint.GetFPID().GetLibItemName())
                netlist_content.append(f"    (comp (ref {ref})")
                netlist_content.append(f"      (value {value})")
                netlist_content.append(f"      (footprint {footprint_name})")
                netlist_content.append("    )")
            netlist_content.append("  )")

            # Nets
            netlist_content.append("  (nets")
            for net_item in board.GetNetInfo().NetsByName():
                net_name = net_item[0]
                if net_name:  # Skip empty net name
                    netlist_content.append(
                        f"    (net (code {net_item[1].GetNetCode()}) (name {net_name})"
                    )

                    # Find connected nodes
                    for footprint in board.GetFootprints():
                        for pad in footprint.Pads():
                            if pad.GetNet() == net_item[1]:
                                ref = footprint.GetReference()
                                pin = pad.GetNumber()
                                netlist_content.append(
                                    f"      (node (ref {ref}) (pin {pin}))"
                                )

                    netlist_content.append("    )")
            netlist_content.append("  )")
            netlist_content.append(")")

        else:
            raise ValueError(f"Unsupported netlist format: {format_type}")

        # Write to file
        with open(output_path, "w") as f:
            f.write("\n".join(netlist_content))

        return output_path

    except Exception as e:
        raise RuntimeError(f"Failed to export netlist: {str(e)}")


def export_pick_and_place(
    board: "pcbnew.BOARD", output_path: str, format_type: str = "csv"
) -> str:
    """
    Export pick and place file.

    Args:
        board: KiCad board object
        output_path: Output file path
        format_type: Format type ("csv", "txt")

    Returns:
        str: Generated file path

    Raises:
        RuntimeError: If operation fails
    """

    try:
        # Create output directory
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)

        # Collect component data
        components = []
        for footprint in board.GetFootprints():
            pos = footprint.GetPosition()
            orientation = footprint.GetOrientation()

            component_data = {
                "reference": footprint.GetReference(),
                "value": footprint.GetValue(),
                "footprint": str(footprint.GetFPID().GetLibItemName()),
                "x_mm": pos.x / 1000000.0,  # Convert to mm
                "y_mm": pos.y / 1000000.0,
                "rotation": orientation.AsDegrees(),
                "layer": "bottom" if footprint.IsFlipped() else "top",
            }
            components.append(component_data)

        # Write file
        if format_type.lower() == "csv":
            import csv

            with open(output_path, "w", newline="") as f:
                writer = csv.DictWriter(
                    f, fieldnames=components[0].keys() if components else []
                )
                writer.writeheader()
                writer.writerows(components)
        else:
            raise ValueError(f"Unsupported pick and place format: {format_type}")

        return output_path

    except Exception as e:
        raise RuntimeError(f"Failed to export pick and place: {str(e)}")
