"""
KiCad PCB Board implementation for CodeToCAD.

This module provides KiCad-specific implementation of PCB board operations.
"""

from codetocad.interfaces.cad.pcb.pcb_board_interface import (
    PCBBoardInterface,
    BoardDimensions,
    DrillSpecs,
)
from codetocad.interfaces.cad.pcb.pcb_layer_interface import PCBLayerInterface
from codetocad.interfaces.cad.pcb.pcb_component_interface import PCBComponentInterface
from codetocad.interfaces.cad.pcb.pcb_net_interface import PCBNetInterface
from codetocad.core.dimensions.length_expression import LengthType
from codetocad.adapters.kicad.kicad_actions.board_operations import (
    create_board,
    set_board_dimensions,
    add_board_layer,
    set_design_rules,
    get_board_info,
    validate_board,
)

from kipy import KiCad


class PCBBoard(PCBBoardInterface):
    """
    KiCad-specific implementation of PCB board operations.

    This class provides KiCad-specific implementations for board management,
    layer handling, and component placement using KiCad's pcbnew API.
    """

    def __init__(self):
        super().__init__()
        self._kicad_board = None

    @property
    def kicad_board(self):
        """Get the underlying KiCad board object."""
        if self._kicad_board is None:
            raise RuntimeError("Board not created. Call create_board() first.")
        return self._kicad_board

    def create_board(
        self, name: str, dimensions: BoardDimensions, layer_count: int = 2
    ) -> "PCBBoardInterface":
        """Create a new KiCad PCB board."""

        try:
            # Create KiCad board
            self._kicad_board = create_board(name)

            # Set board properties
            self.name = name
            self.dimensions = dimensions

            # Set board dimensions and outline
            outline_points = None
            if dimensions.shape.value == "rectangle":
                # Rectangle outline will be created automatically
                pass
            elif dimensions.shape.value == "circle":
                # Create circular outline
                import math

                radius = dimensions.width / 2
                points = []
                for i in range(32):  # 32-sided polygon approximation
                    angle = 2 * math.pi * i / 32
                    x = radius * math.cos(angle)
                    y = radius * math.sin(angle)
                    points.append((x, y))
                points.append(points[0])  # Close the circle
                outline_points = points

            set_board_dimensions(
                self._kicad_board, dimensions.width, dimensions.height, outline_points
            )

            # Set layer count (simplified - KiCad layer management is complex)
            if layer_count not in [2, 4, 6, 8]:
                raise ValueError("Layer count must be 2, 4, 6, or 8")

            # Initialize default design rules
            default_rules = {
                "min_trace_width": 0.1,  # 0.1mm
                "min_via_size": 0.2,  # 0.2mm
                "min_drill_size": 0.1,  # 0.1mm
                "min_spacing": 0.1,  # 0.1mm
            }
            self.set_design_rules(default_rules)

            return self

        except Exception as e:
            raise RuntimeError(f"Failed to create KiCad board: {str(e)}")

    def set_board_outline(
        self, outline_points: list[tuple[float, float]]
    ) -> "PCBBoardInterface":
        """Set custom board outline from points."""

        try:
            if self._kicad_board is None:
                raise RuntimeError("Board not created")

            # Update board dimensions with custom outline
            set_board_dimensions(
                self._kicad_board,
                self.dimensions.width,
                self.dimensions.height,
                outline_points,
            )

            return self

        except Exception as e:
            raise RuntimeError(f"Failed to set board outline: {str(e)}")

    def add_layer(self, layer: PCBLayerInterface) -> "PCBBoardInterface":
        """Add a layer to the board stackup."""

        try:
            if self._kicad_board is None:
                raise RuntimeError("Board not created")

            # Add layer to KiCad board
            layer_id = add_board_layer(
                self._kicad_board,
                layer.properties.name,
                layer.properties.layer_type.value,
            )

            # Add to our layer list
            self.layers.append(layer)

            return self

        except Exception as e:
            raise RuntimeError(f"Failed to add layer: {str(e)}")

    def remove_layer(self, layer_name: str) -> "PCBBoardInterface":
        """Remove a layer from the board stackup."""
        # Layer removal in KiCad is complex and not commonly done
        # This is a simplified implementation
        self.layers = [
            layer for layer in self.layers if layer.properties.name != layer_name
        ]
        return self

    def get_layer(self, layer_name: str) -> PCBLayerInterface | None:
        """Get a layer by name."""
        for layer in self.layers:
            if layer.properties.name == layer_name:
                return layer
        return None

    def set_design_rules(self, rules: dict[str, float]) -> "PCBBoardInterface":
        """Set design rules for the board."""

        try:
            if self._kicad_board is None:
                raise RuntimeError("Board not created")

            # Set design rules in KiCad
            set_design_rules(self._kicad_board, rules)

            # Update our design rules
            self.design_rules.update(rules)

            return self

        except Exception as e:
            raise RuntimeError(f"Failed to set design rules: {str(e)}")

    def add_mounting_hole(
        self, x: LengthType, y: LengthType, drill_specs: DrillSpecs
    ) -> "PCBBoardInterface":
        """Add a mounting hole to the board."""

        try:
            if self._kicad_board is None:
                raise RuntimeError("Board not created")

            # Create mounting hole as a special footprint
            # This is a simplified implementation
            from ..kicad_actions.component_operations import (
                create_footprint,
                place_component,
            )

            # Create mounting hole footprint
            pins = [
                {
                    "number": "1",
                    "name": "MH",
                    "x": 0,
                    "y": 0,
                    "drill_diameter": drill_specs.drill_diameter,
                    "pad_width": drill_specs.finished_hole_diameter,
                    "pad_height": drill_specs.finished_hole_diameter,
                    "shape": "circle",
                }
            ]

            footprint = create_footprint("MountingHoles", "MountingHole", pins)
            place_component(self._kicad_board, footprint, float(x), float(y))

            return self

        except Exception as e:
            raise RuntimeError(f"Failed to add mounting hole: {str(e)}")

    def get_board_area(self) -> float:
        """Calculate the board area."""
        if self.dimensions.shape.value == "rectangle":
            return self.dimensions.width * self.dimensions.height
        elif self.dimensions.shape.value == "circle":
            import math

            radius = self.dimensions.width / 2
            return math.pi * radius * radius
        else:
            # For custom shapes, this would need more complex calculation
            return self.dimensions.width * self.dimensions.height

    def validate_design_rules(self) -> list[str]:
        """Validate the board against design rules."""

        try:
            if self._kicad_board is None:
                return ["Board not created"]

            # Use KiCad's validation
            violations = validate_board(self._kicad_board)

            return violations

        except Exception as e:
            return [f"Validation failed: {str(e)}"]

    def add_component(self, component: PCBComponentInterface) -> "PCBBoardInterface":
        """Add a component to the board."""
        self.components.append(component)
        return self

    def add_net(self, net: PCBNetInterface) -> "PCBBoardInterface":
        """Add a net to the board."""
        self.nets.append(net)
        return self

    def get_info(self) -> dict:
        """Get board information."""

        try:
            if self._kicad_board is None:
                return {"error": "Board not created"}

            return get_board_info(self._kicad_board)

        except Exception as e:
            return {"error": f"Failed to get board info: {str(e)}"}

    def save(self, filepath: str) -> None:
        """Save the board to a file."""

        try:
            if self._kicad_board is None:
                raise RuntimeError("Board not created")

            # Save KiCad board file
            self._kicad_board.Save(filepath)

        except Exception as e:
            raise RuntimeError(f"Failed to save board: {str(e)}")

    def load(self, filepath: str) -> None:
        """Load a board from a file."""

        try:
            # Load KiCad board file using kipy
            kicad_instance = KiCad()
            self._kicad_board = kicad_instance.get_board()

            # Update our properties from loaded board
            info = get_board_info(self._kicad_board)
            self.name = info.get("name", "loaded_board")

        except Exception as e:
            raise RuntimeError(f"Failed to load board: {str(e)}")
