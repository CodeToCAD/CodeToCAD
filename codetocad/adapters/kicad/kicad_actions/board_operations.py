"""
KiCad board operations for CodeToCAD.

This module provides low-level KiCad board management operations using kipy (kicad-python).
"""

from kipy import KiCad
from kipy.board_types import BoardSegment, Net
from kipy.common_types import Vector2, Segment, StrokeAttributes
from kipy.geometry import from_mm
import subprocess
import os


def create_board(name: str = "untitled"):
    """
    Create a new KiCad board or get the currently open board.

    Args:
        name: Board name (used for new boards)

    Returns:
        KiCad board object

    Raises:
        RuntimeError: If operation fails
    """
    try:
        # Connect to running KiCad instance
        kicad_instance = KiCad()

        # Try to get the currently open board
        try:
            board = kicad_instance.get_board()
            return board
        except Exception:
            # If no board is open, we need to create a new one
            # This requires KiCad to be in PCB Editor mode
            # Launch KiCad PCB Editor if needed
            _ensure_kicad_pcb_editor_running()

            # Try again to get the board
            kicad_instance = KiCad()
            board = kicad_instance.get_board()
            return board

    except Exception as e:
        raise RuntimeError(f"Failed to create/get KiCad board: {str(e)}")


def _ensure_kicad_pcb_editor_running():
    """
    Ensure KiCad PCB Editor is running.

    This function attempts to launch KiCad PCB Editor if it's not already running.
    """
    try:
        # Try to find KiCad binary
        kicad_binary = None
        possible_paths = [
            "/Applications/KiCad/KiCad.app/Contents/MacOS/kicad",  # macOS
            "/usr/bin/kicad",  # Linux
            "C:\\Program Files\\KiCad\\bin\\kicad.exe",  # Windows
        ]

        for path in possible_paths:
            if os.path.exists(path):
                kicad_binary = path
                break

        if not kicad_binary:
            # Try to find it in PATH
            try:
                result = subprocess.run(
                    ["which", "kicad"], capture_output=True, text=True
                )
                if result.returncode == 0:
                    kicad_binary = result.stdout.strip()
            except:
                pass

        if kicad_binary:
            # Launch KiCad in background
            subprocess.Popen(
                [kicad_binary], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
            )

    except Exception:
        # If we can't launch KiCad, the user will need to do it manually
        pass


def set_board_dimensions(
    board,
    width: float,
    height: float,
    outline_points: list[tuple[float, float]] | None = None,
) -> None:
    """
    Set board dimensions and outline using Edge.Cuts layer.

    Args:
        board: KiCad board object
        width: Board width in mm
        height: Board height in mm
        outline_points: Custom outline points (if None, creates rectangle)

    Raises:
        RuntimeError: If operation fails
    """
    try:
        if outline_points is None:
            # Create rectangular outline
            outline_points = [
                (-width / 2, -height / 2),
                (width / 2, -height / 2),
                (width / 2, height / 2),
                (-width / 2, height / 2),
                (-width / 2, -height / 2),  # Close the rectangle
            ]

        # Begin a commit transaction for undo/redo support
        commit = board.begin_commit()

        try:
            # Create board outline segments on Edge.Cuts layer
            from kipy.board_types import BoardSegment
            from kipy.common_types import Vector2, StrokeAttributes
            from kipy.geometry import from_mm

            # Edge.Cuts layer ID (typically 44)
            edge_cuts_layer = 44  # BoardLayer.BL_Edge_Cuts

            # Create outline segments
            segments = []
            for i in range(len(outline_points) - 1):
                start_point = outline_points[i]
                end_point = outline_points[i + 1]

                # Create board segment
                segment = BoardSegment()
                segment.layer = edge_cuts_layer

                # Set start and end points (convert mm to nanometers)
                start_vec = Vector2()
                start_vec.x = from_mm(start_point[0])
                start_vec.y = from_mm(start_point[1])

                end_vec = Vector2()
                end_vec.x = from_mm(end_point[0])
                end_vec.y = from_mm(end_point[1])

                # Create the segment shape
                segment_shape = Segment()
                segment_shape.start = start_vec
                segment_shape.end = end_vec

                # Set stroke attributes
                stroke = StrokeAttributes()
                stroke.width = from_mm(0.1)  # 0.1mm line width
                segment_shape.attributes.stroke = stroke

                segments.append(segment)

            # Add segments to board
            if segments:
                board.create_items(segments)

            # Commit the changes
            board.push_commit(commit, f"Set board dimensions {width}x{height}mm")

        except Exception as e:
            # Drop the commit if something went wrong
            board.drop_commit(commit)
            raise e

    except Exception as e:
        raise RuntimeError(f"Failed to set board dimensions: {str(e)}")


def add_board_layer(board, layer_name: str, layer_type: str = "signal") -> int:
    """
    Add a layer to the board stackup.

    Note: Layer management in KiCad is complex and typically done through the board setup.
    This function provides basic layer information but actual layer creation requires
    board stackup modification.

    Args:
        board: KiCad board object
        layer_name: Name of the layer
        layer_type: Type of layer ("signal", "power", "ground", etc.)

    Returns:
        int: Layer ID (placeholder - actual layer creation not implemented)

    Raises:
        RuntimeError: If operation fails
    """
    try:
        # Get current board stackup
        stackup = board.get_stackup()

        # Count existing copper layers
        copper_layer_count = len(
            [layer for layer in stackup.layers if layer.type == 0]
        )  # Copper type

        # For now, return the next available layer ID
        # Actual layer creation would require modifying the board stackup
        # which is a complex operation in KiCad
        next_layer_id = copper_layer_count + 1

        print(
            f"Layer '{layer_name}' of type '{layer_type}' would be created with ID {next_layer_id}"
        )
        print("Note: Actual layer creation requires board stackup modification")

        return next_layer_id

    except Exception as e:
        raise RuntimeError(f"Failed to add board layer: {str(e)}")


def set_design_rules(board, rules: dict[str, float]) -> None:
    """
    Set design rules for the board.

    Note: Design rules in KiCad are complex and typically managed through the
    Design Rules Check (DRC) system. This function provides basic rule information.

    Args:
        board: KiCad board object
        rules: Dictionary of design rules (e.g., {"min_trace_width": 0.1, "min_via_size": 0.2})

    Raises:
        RuntimeError: If operation fails
    """
    try:
        # Design rules in KiCad are typically stored in the project file
        # and managed through the DRC system. The kipy API doesn't directly
        # expose design rule modification methods.

        # For now, we'll log the rules that would be applied
        print("Design rules to be applied:")
        for rule_name, value in rules.items():
            print(f"  {rule_name}: {value} mm")

        print(
            "Note: Design rule modification through kipy API is not directly supported."
        )
        print("Design rules are typically managed through KiCad's Design Rules dialog.")

        # In a full implementation, this would require:
        # 1. Accessing the project's design rules
        # 2. Modifying the DRC constraints
        # 3. Updating the board's design rule checker

    except Exception as e:
        raise RuntimeError(f"Failed to set design rules: {str(e)}")


def get_board_info(board) -> dict:
    """
    Get information about the board using kipy API.

    Args:
        board: KiCad board object

    Returns:
        dict: Board information

    Raises:
        RuntimeError: If operation fails
    """
    try:
        # Get board name
        board_name = board.name

        # Get footprints (components)
        footprints = board.get_footprints()
        component_count = len(footprints)

        # Get nets
        nets = board.get_nets()
        net_count = len(nets)

        # Get stackup for layer information
        stackup = board.get_stackup()
        layer_count = len(stackup.layers)

        # Get title block info
        title_block = board.get_title_block_info()

        info = {
            "name": board_name,
            "layer_count": layer_count,
            "component_count": component_count,
            "net_count": net_count,
            "title": title_block.title,
            "revision": title_block.revision,
            "company": title_block.company,
            "date": title_block.date,
        }

        return info

    except Exception as e:
        raise RuntimeError(f"Failed to get board info: {str(e)}")


def validate_board(board) -> list[str]:
    """
    Validate board against design rules using kipy API.

    Args:
        board: KiCad board object

    Returns:
        list[str]: List of validation errors (empty if valid)

    Raises:
        RuntimeError: If operation fails
    """
    try:
        errors = []

        # Basic validation checks using kipy API
        nets = board.get_nets()
        if len(nets) == 0:
            errors.append("Board has no nets defined")

        footprints = board.get_footprints()
        if len(footprints) == 0:
            errors.append("Board has no components")

        # Check for board outline on Edge.Cuts layer
        shapes = board.get_shapes()
        edge_cuts_layer = 44  # BoardLayer.BL_Edge_Cuts
        edge_items = [shape for shape in shapes if shape.layer == edge_cuts_layer]

        if not edge_items:
            errors.append("Board has no outline defined")

        # Check for unconnected nets (basic connectivity)
        tracks = board.get_tracks()
        if len(tracks) == 0 and len(nets) > 1:
            errors.append("Board has nets but no routing")

        # Additional validation could include:
        # - DRC (Design Rule Check) - would require running KiCad's DRC
        # - Component overlap detection
        # - Via and pad size validation

        return errors

    except Exception as e:
        raise RuntimeError(f"Failed to validate board: {str(e)}")
