"""
KiCad routing operations for CodeToCAD.

This module provides low-level KiCad routing and net management operations using kipy.
"""

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


def create_trace(
    board,
    start_x: float,
    start_y: float,
    end_x: float,
    end_y: float,
    width: float,
    layer: str,
    net_name: str,
) -> "pcbnew.PCB_TRACK":
    """
    Create a trace segment.

    Args:
        board: KiCad board object
        start_x: Start X coordinate in mm
        start_y: Start Y coordinate in mm
        end_x: End X coordinate in mm
        end_y: End Y coordinate in mm
        width: Trace width in mm
        layer: Layer name
        net_name: Net name

    Returns:
        pcbnew.PCB_TRACK: The created trace

    Raises:
        RuntimeError: If operation fails
    """

    try:
        # Get layer ID
        layer_id = board.GetLayerID(layer)
        if layer_id == pcbnew.UNDEFINED_LAYER:
            raise RuntimeError(f"Layer '{layer}' not found")

        # Get or create net
        netlist = board.GetNetInfo()
        net = netlist.GetNetItem(net_name)
        if net is None:
            net = pcbnew.NETINFO_ITEM(board, net_name)
            board.Add(net)

        # Create track
        track = pcbnew.PCB_TRACK(board)
        track.SetStart(
            pcbnew.VECTOR2I(
                int(start_x * 1000000), int(start_y * 1000000)  # Convert mm to nm
            )
        )
        track.SetEnd(pcbnew.VECTOR2I(int(end_x * 1000000), int(end_y * 1000000)))
        track.SetWidth(int(width * 1000000))
        track.SetLayer(layer_id)
        track.SetNet(net)

        # Add to board
        board.Add(track)

        return track

    except Exception as e:
        raise RuntimeError(f"Failed to create trace: {str(e)}")


def create_via(
    board: "pcbnew.BOARD",
    x: float,
    y: float,
    drill_diameter: float,
    pad_diameter: float,
    start_layer: str,
    end_layer: str,
    net_name: str,
) -> "pcbnew.PCB_VIA":
    """
    Create a via.

    Args:
        board: KiCad board object
        x: X coordinate in mm
        y: Y coordinate in mm
        drill_diameter: Drill diameter in mm
        pad_diameter: Pad diameter in mm
        start_layer: Starting layer name
        end_layer: Ending layer name
        net_name: Net name

    Returns:
        pcbnew.PCB_VIA: The created via

    Raises:
        RuntimeError: If operation fails
    """

    try:
        # Get layer IDs
        start_layer_id = board.GetLayerID(start_layer)
        end_layer_id = board.GetLayerID(end_layer)

        if start_layer_id == pcbnew.UNDEFINED_LAYER:
            raise RuntimeError(f"Start layer '{start_layer}' not found")
        if end_layer_id == pcbnew.UNDEFINED_LAYER:
            raise RuntimeError(f"End layer '{end_layer}' not found")

        # Get or create net
        netlist = board.GetNetInfo()
        net = netlist.GetNetItem(net_name)
        if net is None:
            net = pcbnew.NETINFO_ITEM(board, net_name)
            board.Add(net)

        # Create via
        via = pcbnew.PCB_VIA(board)
        via.SetPosition(
            pcbnew.VECTOR2I(int(x * 1000000), int(y * 1000000))  # Convert mm to nm
        )
        via.SetWidth(int(pad_diameter * 1000000))
        via.SetDrill(int(drill_diameter * 1000000))
        via.SetNet(net)

        # Set via type and layers
        if start_layer_id == board.GetLayerID(
            "F.Cu"
        ) and end_layer_id == board.GetLayerID("B.Cu"):
            # Through via
            via.SetViaType(pcbnew.VIATYPE_THROUGH)
        else:
            # Blind/buried via
            via.SetViaType(pcbnew.VIATYPE_BLIND_BURIED)
            via.SetLayerPair(start_layer_id, end_layer_id)

        # Add to board
        board.Add(via)

        return via

    except Exception as e:
        raise RuntimeError(f"Failed to create via: {str(e)}")


def create_arc_trace(
    board: "pcbnew.BOARD",
    start_x: float,
    start_y: float,
    end_x: float,
    end_y: float,
    center_x: float,
    center_y: float,
    width: float,
    layer: str,
    net_name: str,
) -> "pcbnew.PCB_ARC":
    """
    Create an arc trace segment.

    Args:
        board: KiCad board object
        start_x: Start X coordinate in mm
        start_y: Start Y coordinate in mm
        end_x: End X coordinate in mm
        end_y: End Y coordinate in mm
        center_x: Arc center X coordinate in mm
        center_y: Arc center Y coordinate in mm
        width: Trace width in mm
        layer: Layer name
        net_name: Net name

    Returns:
        pcbnew.PCB_ARC: The created arc trace

    Raises:
        RuntimeError: If operation fails
    """

    try:
        # Get layer ID
        layer_id = board.GetLayerID(layer)
        if layer_id == pcbnew.UNDEFINED_LAYER:
            raise RuntimeError(f"Layer '{layer}' not found")

        # Get or create net
        netlist = board.GetNetInfo()
        net = netlist.GetNetItem(net_name)
        if net is None:
            net = pcbnew.NETINFO_ITEM(board, net_name)
            board.Add(net)

        # Create arc
        arc = pcbnew.PCB_ARC(board)
        arc.SetStart(pcbnew.VECTOR2I(int(start_x * 1000000), int(start_y * 1000000)))
        arc.SetEnd(pcbnew.VECTOR2I(int(end_x * 1000000), int(end_y * 1000000)))
        arc.SetCenter(pcbnew.VECTOR2I(int(center_x * 1000000), int(center_y * 1000000)))
        arc.SetWidth(int(width * 1000000))
        arc.SetLayer(layer_id)
        arc.SetNet(net)

        # Add to board
        board.Add(arc)

        return arc

    except Exception as e:
        raise RuntimeError(f"Failed to create arc trace: {str(e)}")


def route_net_auto(
    board: "pcbnew.BOARD", net_name: str, algorithm: str = "shortest"
) -> list["pcbnew.BOARD_ITEM"]:
    """
    Automatically route a net (simplified implementation).

    Args:
        board: KiCad board object
        net_name: Net name to route
        algorithm: Routing algorithm ("shortest", "avoid_vias")

    Returns:
        list[pcbnew.BOARD_ITEM]: Created routing items

    Raises:
        RuntimeError: If operation fails
    """

    try:
        # This is a simplified auto-router implementation
        # A full implementation would use KiCad's routing algorithms
        # or external routing engines

        netlist = board.GetNetInfo()
        net = netlist.GetNetItem(net_name)
        if net is None:
            raise RuntimeError(f"Net '{net_name}' not found")

        # Find all pads connected to this net
        pads = []
        for footprint in board.GetFootprints():
            for pad in footprint.Pads():
                if pad.GetNet() == net:
                    pads.append(pad)

        if len(pads) < 2:
            return []  # Nothing to route

        # Simple point-to-point routing
        routed_items = []
        for i in range(len(pads) - 1):
            start_pad = pads[i]
            end_pad = pads[i + 1]

            start_pos = start_pad.GetPosition()
            end_pos = end_pad.GetPosition()

            # Create straight trace between pads
            track = create_trace(
                board,
                start_pos.x / 1000000.0,  # Convert to mm
                start_pos.y / 1000000.0,
                end_pos.x / 1000000.0,
                end_pos.y / 1000000.0,
                0.2,  # Default trace width
                "F.Cu",  # Default layer
                net_name,
            )
            routed_items.append(track)

        return routed_items

    except Exception as e:
        raise RuntimeError(f"Failed to auto-route net: {str(e)}")


def check_design_rules(board: "pcbnew.BOARD") -> list[str]:
    """
    Check design rules (simplified implementation).

    Args:
        board: KiCad board object

    Returns:
        list[str]: List of design rule violations

    Raises:
        RuntimeError: If operation fails
    """

    try:
        violations = []

        # This is a simplified DRC implementation
        # KiCad has a full DRC engine that could be used

        design_settings = board.GetDesignSettings()
        min_trace_width = design_settings.m_TrackMinWidth / 1000000.0  # Convert to mm
        min_clearance = design_settings.m_MinClearance / 1000000.0

        # Check trace widths
        for track in board.GetTracks():
            if isinstance(track, pcbnew.PCB_TRACK):
                width = track.GetWidth() / 1000000.0
                if width < min_trace_width:
                    violations.append(
                        f"Trace width {width:.3f}mm is below minimum {min_trace_width:.3f}mm"
                    )

        # Check via sizes
        for track in board.GetTracks():
            if isinstance(track, pcbnew.PCB_VIA):
                drill = track.GetDrill() / 1000000.0
                min_drill = design_settings.m_ViasMinDrill / 1000000.0
                if drill < min_drill:
                    violations.append(
                        f"Via drill {drill:.3f}mm is below minimum {min_drill:.3f}mm"
                    )

        # Additional checks could include:
        # - Clearance violations
        # - Unconnected nets
        # - Overlapping components
        # - Board outline violations

        return violations

    except Exception as e:
        raise RuntimeError(f"Failed to check design rules: {str(e)}")


def get_net_info(board: "pcbnew.BOARD", net_name: str) -> dict[str, Any]:
    """
    Get information about a net.

    Args:
        board: KiCad board object
        net_name: Net name

    Returns:
        dict[str, Any]: Net information

    Raises:
        RuntimeError: If operation fails
    """

    try:
        netlist = board.GetNetInfo()
        net = netlist.GetNetItem(net_name)

        if net is None:
            raise RuntimeError(f"Net '{net_name}' not found")

        # Count connected pads
        pad_count = 0
        for footprint in board.GetFootprints():
            for pad in footprint.Pads():
                if pad.GetNet() == net:
                    pad_count += 1

        # Count tracks and vias
        track_count = 0
        via_count = 0
        total_length = 0.0

        for track in board.GetTracks():
            if track.GetNet() == net:
                if isinstance(track, pcbnew.PCB_VIA):
                    via_count += 1
                else:
                    track_count += 1
                    # Calculate track length
                    start = track.GetStart()
                    end = track.GetEnd()
                    length = (
                        (end.x - start.x) ** 2 + (end.y - start.y) ** 2
                    ) ** 0.5 / 1000000.0
                    total_length += length

        info = {
            "name": net_name,
            "net_code": net.GetNetCode(),
            "pad_count": pad_count,
            "track_count": track_count,
            "via_count": via_count,
            "total_length_mm": total_length,
            "is_routed": track_count > 0 or via_count > 0,
        }

        return info

    except Exception as e:
        raise RuntimeError(f"Failed to get net info: {str(e)}")
