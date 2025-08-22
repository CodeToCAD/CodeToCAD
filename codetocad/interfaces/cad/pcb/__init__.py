"""
PCB design interfaces for CodeToCAD.

This module provides abstract interfaces for PCB design operations including
board management, component placement, routing, and export functionality.
"""

from codetocad.interfaces.cad.pcb.pcb_board_interface import (
    PCBBoardInterface,
    BoardDimensions,
    BoardShape,
    DrillSpecs,
)
from codetocad.interfaces.cad.pcb.pcb_component_interface import (
    PCBComponentInterface,
    ComponentType,
    MountType,
    PinDefinition,
    FootprintDefinition,
    ElectricalProperties,
)
from codetocad.interfaces.cad.pcb.pcb_routing_interface import (
    PCBRoutingInterface,
    TraceShape,
    ViaType,
    TraceSegment,
    ViaDefinition,
    RoutingConstraints,
)
from codetocad.interfaces.cad.pcb.pcb_export_interface import (
    PCBExportInterface,
    ExportFormat,
    GerberOptions,
    DrillOptions,
    ExportOptions,
)
from codetocad.interfaces.cad.pcb.pcb_layer_interface import (
    PCBLayerInterface,
    LayerType,
    LayerSide,
    LayerProperties,
)
from codetocad.interfaces.cad.pcb.pcb_net_interface import (
    PCBNetInterface,
    NetClass,
    NetConstraints,
    NetConnection,
)
from codetocad.interfaces.cad.pcb.component_presets import (
    ComponentPresetsInterface,
    ResistorPresets,
    CapacitorPresets,
    LEDPresets,
    TransistorPresets,
    ICPresets,
    ConnectorPresets,
)
