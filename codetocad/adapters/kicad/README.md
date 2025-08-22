# KiCad Adapter for CodeToCAD

This adapter provides PCB design capabilities using kipy (kicad-python) - the modern KiCad Python API.

## KiCad-Python (kipy) Support

The adapter uses kipy/kicad-python exclusively:

- **Package**: `kicad-python` (install via `pip install kicad-python`)
- **Requirements**: KiCad 9.0+ running with API enabled in Preferences > Plugins
- **Advantages**: Modern, actively developed, real-time interaction with running KiCad
- **Use Case**: Interactive development, real-time PCB updates

## Features

- **Board Management**: Create and manage PCB boards with custom dimensions and layer stackups
- **Component Placement**: Place electronic components with preset footprints and properties
- **Routing Operations**: Create traces, vias, and manage nets with design rule checking
- **Export Functionality**: Generate Gerber files, drill files, and manufacturing outputs
- **Component Presets**: Access to common electronic components (resistors, capacitors, LEDs, etc.)
- **Modern API**: Uses kipy/kicad-python exclusively

## Requirements

- KiCad 9.0 or later
- `kicad-python` package: `pip install kicad-python`
- KiCad running with API enabled in Preferences > Plugins
- Python 3.9 or later

## Installation

1. Install KiCad 9.0+:
   - **Windows**: Download from [KiCad website](https://www.kicad.org/download/)
   - **macOS**: `brew install kicad`
   - **Linux**: `sudo apt install kicad` (Ubuntu/Debian) or equivalent

2. Install kicad-python package:
   ```bash
   pip install kicad-python
   ```

3. Enable API in KiCad: Preferences > Plugins > Enable API Server

## Checking API Availability

You can check if kipy is available:

```python
try:
    from kipy import KiCad
    print("✅ kipy (kicad-python) is available")
except ImportError:
    try:
        from kicad import KiCad
        print("✅ kicad-python is available")
    except ImportError:
        print("❌ kicad-python is not available")
        print("Install with: pip install kicad-python")
```

## Usage Examples

### Basic PCB Creation

```python
from codetocad.adapters.kicad.pcb import PCBBoard, PCBComponent
from codetocad.interfaces.cad.pcb import BoardDimensions, BoardShape

# Create a new PCB board
board = PCBBoard()
dimensions = BoardDimensions(width=50.0, height=40.0, thickness=1.6)
board.create_board("my_pcb", dimensions, layer_count=2)

# Add components using presets
resistor = PCBComponent.preset.resistor.smd_0603("10k")
resistor.set_position(10, 10)
board.add_component(resistor)

led = PCBComponent.preset.led.red_0603()
led.set_position(20, 10)
board.add_component(led)
```

### Component Presets

```python
from codetocad.adapters.kicad.pcb import PCBComponent

# Resistors
r1 = PCBComponent.preset.resistor.smd_0603("10k", tolerance="1%")
r2 = PCBComponent.preset.resistor.through_hole("4.7k", power_rating="0.5W")

# Capacitors
c1 = PCBComponent.preset.capacitor.ceramic_0805("100nF", voltage="50V")
c2 = PCBComponent.preset.capacitor.electrolytic_tht("1000uF", voltage="25V")

# LEDs
led1 = PCBComponent.preset.led.red_0603()
led2 = PCBComponent.preset.led.rgb_5050()

# Transistors
q1 = PCBComponent.preset.transistor.npn_bjt_sot23("2N3904")
q2 = PCBComponent.preset.transistor.n_channel_mosfet_sot23("2N7002")

# ICs
u1 = PCBComponent.preset.ic.logic_gate_dip14("74HC00")
u2 = PCBComponent.preset.ic.microcontroller_qfp32("STM32F103")

# Connectors
j1 = PCBComponent.preset.connector.pin_header_1x2()
j2 = PCBComponent.preset.connector.usb_a_female()
```

### Routing and Nets

```python
from codetocad.adapters.kicad.pcb import PCBNet, PCBRouting
from codetocad.interfaces.cad.pcb import NetClass, ViaType

# Create nets
vcc_net = PCBNet("VCC")
vcc_net.set_net_class(NetClass.POWER)

gnd_net = PCBNet("GND") 
gnd_net.set_net_class(NetClass.GROUND)

# Connect components to nets
resistor.connect_pin_to_net("1", "VCC")
resistor.connect_pin_to_net("2", "LED_ANODE")

led.connect_pin_to_net("A", "LED_ANODE")
led.connect_pin_to_net("K", "GND")

# Add routing
routing = PCBRouting()
routing.add_trace(10, 10, 20, 10, 0.2, "top", "LED_ANODE")
routing.add_via(15, 10, ViaType.THROUGH, 0.2, 0.5, "top", "bottom", "LED_ANODE")
```

### Export for Manufacturing

```python
from codetocad.adapters.kicad.pcb import PCBExport
from codetocad.interfaces.cad.pcb import ExportFormat

# Create export handler
exporter = PCBExport(board)

# Export Gerber files
gerber_files = exporter.export_gerbers("./output/gerbers")

# Export drill files
drill_files = exporter.export_drill_files("./output/drill")

# Export pick and place
pnp_file = exporter.export_pick_and_place("./output/assembly.csv")

# Export 3D model
step_file = exporter.export_3d_model("./output/pcb.step", ExportFormat.STEP)

# Create complete manufacturing package
package = exporter.create_manufacturing_package("./output/manufacturing")
```

## Architecture

The KiCad adapter follows CodeToCAD's standard adapter pattern:

```
codetocad/adapters/kicad/
├── __init__.py                 # Main adapter module
├── README.md                   # This file
├── pcb/                        # PCB-specific implementations
│   ├── __init__.py
│   ├── pcb_board.py           # Board management
│   ├── pcb_component.py       # Component placement
│   ├── pcb_routing.py         # Routing operations
│   ├── pcb_export.py          # Export functionality
│   ├── pcb_layer.py           # Layer management
│   └── pcb_net.py             # Net management
├── kicad_actions/             # Low-level KiCad operations
│   ├── __init__.py
│   ├── board_operations.py    # Board-level operations
│   ├── component_operations.py # Component operations
│   ├── routing_operations.py  # Routing operations
│   └── export_operations.py   # Export operations
└── examples/                  # Usage examples
    ├── __init__.py
    ├── basic_pcb.py          # Basic PCB creation
    ├── component_placement.py # Component examples
    └── manufacturing_export.py # Export examples
```

## Error Handling

The adapter includes comprehensive error handling:

- **Missing KiCad**: Graceful fallback with informative error messages
- **Version Compatibility**: Checks for compatible KiCad versions
- **API Errors**: Wraps KiCad API exceptions with user-friendly messages
- **Validation**: Validates inputs before calling KiCad APIs

## Limitations

- Requires KiCad installation with Python support
- Some advanced KiCad features may not be exposed
- 3D model export requires KiCad's 3D libraries
- Schematic integration is limited (primarily netlist-based)

## Contributing

When adding new features:

1. Follow the existing interface patterns
2. Add comprehensive error handling
3. Include unit tests with mocks for KiCad dependencies
4. Update documentation and examples
5. Test with multiple KiCad versions when possible

## References

- [KiCad Python API Documentation](https://docs.kicad.org/doxygen/)
- [KiCad Plugin Development](https://docs.kicad.org/doxygen/md_Documentation_development_pcbnew-plugins.html)
- [pcbnew Python Reference](https://docs.kicad.org/doxygen/namespacepcbnew.html)
