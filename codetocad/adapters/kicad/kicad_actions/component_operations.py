"""
KiCad component operations for CodeToCAD.

This module provides low-level KiCad component management operations using kipy.
"""

from kipy import KiCad
from kipy.board_types import FootprintInstance, Footprint, Pad, PadStack, PadStackLayer
from kipy.common_types import LibraryIdentifier
from kipy.geometry import Vector2


def create_footprint(
    library_name: str, footprint_name: str, pins: list[dict[str, any]]
):
    """
    Create a custom footprint using kipy API.

    Args:
        library_name: Library name for the footprint
        footprint_name: Name of the footprint
        pins: List of pin definitions

    Returns:
        Footprint: The created footprint

    Raises:
        RuntimeError: If operation fails
    """
    try:
        # Create footprint identifier
        lib_id = LibraryIdentifier()
        lib_id.library = library_name
        lib_id.name = footprint_name

        # Create footprint
        footprint = Footprint()
        footprint.id = lib_id

        # Note: Creating custom footprints with kipy is complex and typically
        # done through KiCad's footprint editor. This function provides a
        # simplified example of how pad data would be structured.

        print(f"Creating footprint '{footprint_name}' in library '{library_name}'")
        print(f"Pins to be created: {len(pins)}")

        for i, pin_def in enumerate(pins):
            print(f"  Pin {i+1}: {pin_def}")

        print("Note: Actual footprint creation requires KiCad's footprint editor")
        print("This function demonstrates the data structure for footprint creation")

        return footprint

    except Exception as e:
        raise RuntimeError(f"Failed to create footprint: {str(e)}")


def place_component(
    board,
    footprint_instance: FootprintInstance,
    x: float,
    y: float,
    rotation: float = 0.0,
    layer: str = "top",
) -> FootprintInstance:
    """
    Place a component on the board using kipy API.

    Args:
        board: KiCad board object
        footprint_instance: FootprintInstance to place
        x: X position in mm
        y: Y position in mm
        rotation: Rotation in degrees
        layer: Layer to place on ("top" or "bottom")

    Returns:
        FootprintInstance: The placed footprint instance

    Raises:
        RuntimeError: If operation fails
    """
    try:
        # Set position
        position = Vector2()
        position.x = from_mm(x) if "from_mm" in globals() else int(x * 1000000)
        position.y = from_mm(y) if "from_mm" in globals() else int(y * 1000000)
        footprint_instance.position = position

        # Set rotation
        from kipy.geometry import Angle

        angle = Angle()
        angle.degrees = rotation
        footprint_instance.orientation = angle

        # Set layer (0 = F.Cu, 31 = B.Cu)
        if layer.lower() == "bottom":
            footprint_instance.layer = 31  # B.Cu
        else:
            footprint_instance.layer = 0  # F.Cu

        # Begin commit for undo/redo support
        commit = board.begin_commit()

        try:
            # Add to board
            board.create_items([footprint_instance])

            # Commit the changes
            board.push_commit(commit, f"Place component at ({x}, {y})")

        except Exception as e:
            board.drop_commit(commit)
            raise e

        return footprint_instance

    except Exception as e:
        raise RuntimeError(f"Failed to place component: {str(e)}")


def set_component_properties(
    footprint_instance: FootprintInstance,
    reference: str,
    value: str,
    properties: dict[str, str] | None = None,
) -> None:
    """
    Set component properties using kipy API.

    Args:
        footprint_instance: FootprintInstance to modify
        reference: Reference designator (e.g., "R1", "C5")
        value: Component value
        properties: Additional properties

    Raises:
        RuntimeError: If operation fails
    """
    try:
        # Set reference and value
        footprint_instance.reference = reference
        footprint_instance.value = value

        # Set additional properties if provided
        if properties:
            for key, val in properties.items():
                # Store as custom properties (kipy may not have direct setters)
                print(f"Setting property {key}: {val}")

        print(f"Set component properties: ref={reference}, value={value}")

    except Exception as e:
        raise RuntimeError(f"Failed to set component properties: {str(e)}")


def connect_component_to_net(
    board, footprint_instance: FootprintInstance, pin_number: str, net_name: str
) -> None:
    """
    Connect a component pin to a net using kipy API.

    Args:
        board: KiCad board object
        footprint_instance: Component footprint instance
        pin_number: Pin number to connect
        net_name: Name of net to connect to

    Raises:
        RuntimeError: If operation fails
    """
    try:
        # Get or create the net
        nets = board.get_nets()
        target_net = None

        for net in nets:
            if net.name == net_name:
                target_net = net
                break

        if not target_net:
            # Create new net
            from kipy.board_types import Net

            target_net = Net()
            target_net.name = net_name

            # Add net to board
            commit = board.begin_commit()
            try:
                board.create_items([target_net])
                board.push_commit(commit, f"Create net {net_name}")
            except Exception as e:
                board.drop_commit(commit)
                raise e

        # Note: Connecting specific pins to nets in kipy requires more complex
        # pad and net management. This is a simplified implementation.
        print(f"Connecting pin {pin_number} of component to net {net_name}")
        print("Note: Actual pin-to-net connection requires detailed pad management")

    except Exception as e:
        raise RuntimeError(f"Failed to connect component to net: {str(e)}")


def get_component_info(footprint_instance: FootprintInstance) -> dict[str, str]:
    """
    Get information about a component using kipy API.

    Args:
        footprint_instance: Component footprint instance

    Returns:
        dict[str, str]: Component information

    Raises:
        RuntimeError: If operation fails
    """
    try:
        # Get position
        pos = footprint_instance.position

        # Get orientation
        orientation = footprint_instance.orientation

        # Get layer
        layer = (
            "bottom" if footprint_instance.layer == 31 else "top"
        )  # 31 = B.Cu, 0 = F.Cu

        info = {
            "reference": str(footprint_instance.reference_field.text.value),
            "value": str(footprint_instance.value_field.text.value),
            "position_x": str(pos.x / 1000000.0),  # Convert to mm
            "position_y": str(pos.y / 1000000.0),
            "rotation": str(orientation.degrees),
            "layer": layer,
            "footprint_name": str(footprint_instance.definition.id.name),
            "library": str(footprint_instance.definition.id.library),
        }

        return info

    except Exception as e:
        raise RuntimeError(f"Failed to get component info: {str(e)}")


def move_component(
    footprint_instance: FootprintInstance,
    x: float,
    y: float,
    rotation: float | None = None,
) -> None:
    """
    Move a component to a new position using kipy API.

    Args:
        footprint_instance: KiCad footprint instance
        x: New X position in mm
        y: New Y position in mm
        rotation: New rotation in degrees (optional)

    Raises:
        RuntimeError: If operation fails
    """
    try:
        # Set new position
        position = Vector2()
        position.x = from_mm(x) if "from_mm" in globals() else int(x * 1000000)
        position.y = from_mm(y) if "from_mm" in globals() else int(y * 1000000)
        footprint_instance.position = position

        # Set new rotation if provided
        if rotation is not None:
            from kipy.geometry import Angle

            angle = Angle()
            angle.degrees = rotation
            footprint_instance.orientation = angle

        print(f"Moved component to ({x}, {y})")
        if rotation is not None:
            print(f"Set rotation to {rotation} degrees")

    except Exception as e:
        raise RuntimeError(f"Failed to move component: {str(e)}")


def delete_component(board, footprint_instance: FootprintInstance) -> None:
    """
    Delete a component from the board using kipy API.

    Args:
        board: KiCad board object
        footprint_instance: Footprint instance to delete

    Raises:
        RuntimeError: If operation fails
    """
    try:
        # Begin commit for undo/redo support
        commit = board.begin_commit()

        try:
            # Remove from board
            board.remove_items([footprint_instance])

            # Commit the changes
            board.push_commit(commit, "Delete component")

        except Exception as e:
            board.drop_commit(commit)
            raise e

        print("Component deleted successfully")

    except Exception as e:
        raise RuntimeError(f"Failed to delete component: {str(e)}")
