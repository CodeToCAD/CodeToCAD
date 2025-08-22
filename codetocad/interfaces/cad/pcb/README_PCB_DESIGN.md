# PCB Design Interface for CodeToCAD

This document describes the comprehensive PCB design interface implemented for CodeToCAD, providing programmatic PCB design capabilities using KiCad as the primary backend.

## Overview

The PCB design interface extends CodeToCAD's capabilities to include electronic circuit board design, enabling users to:

- Create and manage PCB boards with custom dimensions and layer stackups
- Place electronic components using preset libraries or custom definitions
- Route traces and manage nets with design rule checking
- Export manufacturing files (Gerber, drill files, pick & place, BOM)
- Integrate PCB designs with 3D mechanical CAD workflows

## Architecture

The implementation follows CodeToCAD's standard adapter pattern:

```
codetocad/
├── interfaces/cad/pcb/           # Abstract interfaces
│   ├── pcb_board_interface.py    # Board management
│   ├── pcb_component_interface.py # Component placement
│   ├── pcb_routing_interface.py   # Routing operations
│   ├── pcb_export_interface.py    # Export functionality
│   ├── pcb_layer_interface.py     # Layer management
│   ├── pcb_net_interface.py       # Net management
│   └── component_presets/         # Component preset system
│       ├── resistor_presets.py    # Resistor components
│       ├── capacitor_presets.py   # Capacitor components
│       ├── led_presets.py         # LED components
│       ├── transistor_presets.py  # Transistor components
│       ├── ic_presets.py          # IC components
│       └── connector_presets.py   # Connector components
└── adapters/kicad/               # KiCad-specific implementation
    ├── pcb/                      # PCB implementations
    ├── kicad_actions/            # Low-level KiCad operations
    └── examples/                 # Usage examples
```

## Key Features

### 1. Abstract Interface Design

The PCB interfaces are designed to be CAD-system agnostic:

- **PCBBoardInterface**: Board creation, dimensions, layer stackup
- **PCBComponentInterface**: Component placement and properties
- **PCBRoutingInterface**: Trace routing, vias, design rules
- **PCBExportInterface**: Manufacturing file generation
- **PCBLayerInterface**: Layer management and properties
- **PCBNetInterface**: Net connectivity and constraints

### 2. Component Preset System

Comprehensive preset system for common electronic components:

```python
# Resistors
resistor = PCBComponent.preset.resistor.smd_0603("10k", tolerance="1%")
resistor_tht = PCBComponent.preset.resistor.through_hole("4.7k", power_rating="0.5W")

# Capacitors
cap_ceramic = PCBComponent.preset.capacitor.ceramic_0805("100nF", voltage="50V")
cap_electrolytic = PCBComponent.preset.capacitor.electrolytic_tht("1000uF", voltage="25V")

# LEDs
led_red = PCBComponent.preset.led.red_0603()
led_rgb = PCBComponent.preset.led.rgb_5050()

# Transistors
transistor_npn = PCBComponent.preset.transistor.npn_bjt_sot23("2N3904")
mosfet = PCBComponent.preset.transistor.n_channel_mosfet_sot23("2N7002")

# ICs
logic_gate = PCBComponent.preset.ic.logic_gate_dip14("74HC00")
microcontroller = PCBComponent.preset.ic.microcontroller_qfp32("STM32F103")

# Connectors
header = PCBComponent.preset.connector.pin_header_1x2()
usb = PCBComponent.preset.connector.usb_a_female()
```

### 3. KiCad Integration

The KiCad adapter provides:

- **Modern API**: Uses kipy/kicad-python exclusively
- **Error Handling**: Comprehensive error messages and recovery
- **Modular Operations**: Low-level operations in `kicad_actions/`
- **Version Compatibility**: Supports KiCad 9.0+ with API enabled

### 4. Manufacturing Export

Complete manufacturing package generation:

```python
exporter = PCBExport(board)

# Export individual file types
gerber_files = exporter.export_gerbers("./gerbers")
drill_files = exporter.export_drill_files("./drill")
pnp_file = exporter.export_pick_and_place("./assembly.csv")
bom_file = exporter.export_bill_of_materials("./bom.csv")
step_file = exporter.export_3d_model("./pcb.step")

# Or create complete manufacturing package
package = exporter.create_manufacturing_package("./manufacturing")
```

## Usage Examples

### Basic PCB Creation

```python
from codetocad.adapters.kicad.pcb import PCBBoard, PCBComponent, PCBNet
from codetocad.interfaces.cad.pcb import BoardDimensions, BoardShape

# Create board
board = PCBBoard()
dimensions = BoardDimensions(width=50.0, height=40.0, thickness=1.6)
board.create_board("led_circuit", dimensions, layer_count=2)

# Add components
led = PCBComponent.preset.led.red_0603()
led.reference_designator = "D1"
led.set_position(10, 0)
board.add_component(led)

resistor = PCBComponent.preset.resistor.smd_0603("330")
resistor.reference_designator = "R1"
resistor.set_position(-10, 0)
board.add_component(resistor)

# Create nets and connections
vcc_net = PCBNet("VCC", board)
gnd_net = PCBNet("GND", board)
led_anode_net = PCBNet("LED_ANODE", board)

resistor.connect_pin_to_net("1", "VCC")
resistor.connect_pin_to_net("2", "LED_ANODE")
led.connect_pin_to_net("A", "LED_ANODE")
led.connect_pin_to_net("K", "GND")
```

### Advanced Routing

```python
from codetocad.adapters.kicad.pcb import PCBRouting
from codetocad.interfaces.cad.pcb import ViaType

routing = PCBRouting(board)

# Add traces
routing.add_trace(
    start_x=-8, start_y=0,
    end_x=8, end_y=0,
    width=0.3,
    layer="F.Cu",
    net_name="LED_ANODE"
)

# Add vias
routing.add_via(
    x=10, y=-2,
    via_type=ViaType.THROUGH,
    drill_diameter=0.2,
    pad_diameter=0.4,
    start_layer="F.Cu",
    end_layer="B.Cu",
    net_name="GND"
)

# Auto-route nets
routing.route_net(vcc_net, algorithm="shortest")
```

## Research Findings

### Open Source PCB Tools with Python APIs

1. **KiCad** (Primary Choice)
   - Mature, professional-grade PCB design tool
   - Comprehensive Python API (pcbnew module)
   - Active development and community
   - Cross-platform support
   - Extensive component libraries

2. **OpenEMS/PyEMS**
   - Electromagnetic simulation capabilities
   - Python interface for field simulations
   - Complementary to KiCad for RF/microwave designs

3. **SKiDL**
   - Python-based schematic capture
   - Generates netlists for KiCad
   - Programmatic circuit description

4. **FreeCAD PCB Workbench**
   - Limited PCB capabilities
   - More focused on mechanical integration
   - Less mature than KiCad

### Design Decisions

- **KiCad as Primary Backend**: Most mature and feature-complete
- **Modular Architecture**: Easy to add other backends later
- **Preset System**: Reduces complexity for common components
- **Graceful Degradation**: Works without KiCad (limited functionality)

## Integration with CodeToCAD

### Material System Integration

PCB components can specify material properties:

```python
# Component materials integrate with CodeToCAD's material system
component.electrical_properties.custom_properties["material"] = "FR4"
component.electrical_properties.custom_properties["copper_thickness"] = "1oz"
```

### 3D CAD Workflow Integration

PCB designs can be exported as 3D models for mechanical integration:

```python
# Export PCB as STEP file for mechanical CAD
step_file = exporter.export_3d_model("pcb.step", include_components=True)

# Import into 3D CAD workflow
from codetocad.adapters.build123d import Part
pcb_part = Part.import_step(step_file)
```

## Testing Strategy

Comprehensive testing approach:

1. **Unit Tests**: Mock KiCad dependencies for interface testing
2. **Integration Tests**: Test with actual KiCad installation
3. **Example Tests**: Validate usage examples work correctly
4. **Error Handling Tests**: Verify graceful failure modes

## Future Enhancements

1. **Additional Backends**: Support for other PCB tools
2. **Schematic Integration**: Full schematic capture capabilities
3. **Simulation Integration**: SPICE simulation support
4. **Advanced Routing**: Differential pairs, length matching
5. **Component Libraries**: Expanded preset collections
6. **Design Rule Checking**: Enhanced DRC capabilities

## Installation and Requirements

### KiCad Installation

```bash
# macOS
brew install kicad

# Ubuntu/Debian
sudo apt install kicad

# Windows
# Download from https://www.kicad.org/download/
```

### Python Dependencies

The PCB interface requires kicad-python for full functionality.

```bash
# Install kicad-python
pip install kicad-python
```

```python
# Check kipy availability
try:
    from kipy import KiCad
    print("✅ kipy (kicad-python) is available")
except ImportError:
    try:
        from kicad import KiCad
        print("✅ kicad-python is available")
    except ImportError:
        print("❌ kicad-python is not available")
```

## Contributing

When contributing to the PCB interface:

1. Follow existing interface patterns
2. Add comprehensive error handling
3. Include unit tests with mocks
4. Update documentation and examples
5. Test with multiple KiCad versions when possible

## References

- [KiCad Python API Documentation](https://docs.kicad.org/doxygen/)
- [KiCad Plugin Development Guide](https://docs.kicad.org/doxygen/md_Documentation_development_pcbnew-plugins.html)
- [OpenEMS Documentation](https://openems.de/)
- [SKiDL Documentation](https://devbisme.github.io/skidl/)

---

This PCB design interface represents a significant expansion of CodeToCAD's capabilities, enabling comprehensive electronic design automation while maintaining the framework's core principles of programmatic design and adapter-based architecture.
