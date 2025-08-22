"""
Basic PCB creation example using KiCad adapter.

This example demonstrates how to create a simple PCB board with
basic components and routing using CodeToCAD's KiCad adapter.
"""

from codetocad.adapters.kicad import *


def basic_pcb_example():
    """
    Create a basic PCB with LED and resistor circuit.

    This example creates a simple LED circuit with:
    - 50mm x 40mm rectangular board
    - LED component
    - Current limiting resistor
    - Power and ground connections
    - Basic routing
    """

    try:
        # Create board
        print("Creating PCB board...")
        board = PCBBoard()

        # Define board dimensions
        dimensions = BoardDimensions(
            width=50.0,  # 50mm width
            height=40.0,  # 40mm height
            thickness=1.6,  # Standard PCB thickness
            shape=BoardShape.RECTANGLE,
        )

        # Create the board
        board.create_board("led_circuit", dimensions, layer_count=2)

        # Set design rules
        design_rules = {
            "min_trace_width": 0.2,  # 0.2mm minimum trace width
            "min_via_size": 0.4,  # 0.4mm minimum via size
            "min_drill_size": 0.2,  # 0.2mm minimum drill size
            "min_spacing": 0.15,  # 0.15mm minimum spacing
        }
        board.set_design_rules(design_rules)

        print(f"Board created: {board.name}")
        print(f"Board area: {board.get_board_area():.2f} mm²")

        # Create components using presets
        print("Adding components...")

        # LED component
        led = PCBComponent.preset.led.red_0603()
        led.reference_designator = "D1"
        led.set_position(10, 0)  # Position at 10mm, 0mm
        board.add_component(led)

        # Current limiting resistor
        resistor = PCBComponent.preset.resistor.smd_0603("330", tolerance="5%")
        resistor.reference_designator = "R1"
        resistor.set_position(-10, 0)  # Position at -10mm, 0mm
        board.add_component(resistor)

        # Power connector
        power_conn = PCBComponent.preset.connector.pin_header_1x2()
        power_conn.reference_designator = "J1"
        power_conn.set_position(0, -15)  # Position at 0mm, -15mm
        board.add_component(power_conn)

        print(f"Added {len(board.components)} components")

        # Create nets
        print("Creating nets...")

        # VCC net (power)
        vcc_net = PCBNet("VCC", board)
        vcc_net.set_net_class(NetClass.POWER)
        board.add_net(vcc_net)

        # GND net (ground)
        gnd_net = PCBNet("GND", board)
        gnd_net.set_net_class(NetClass.GROUND)
        board.add_net(gnd_net)

        # LED_ANODE net (signal)
        led_anode_net = PCBNet("LED_ANODE", board)
        led_anode_net.set_net_class(NetClass.SIGNAL)
        board.add_net(led_anode_net)

        # Connect components to nets
        print("Connecting components...")

        # Power connector connections
        power_conn.connect_pin_to_net("1", "VCC")
        power_conn.connect_pin_to_net("2", "GND")

        # Resistor connections
        resistor.connect_pin_to_net("1", "VCC")
        resistor.connect_pin_to_net("2", "LED_ANODE")

        # LED connections
        led.connect_pin_to_net("A", "LED_ANODE")  # Anode
        led.connect_pin_to_net("K", "GND")  # Cathode

        print(f"Created {len(board.nets)} nets")

        # Add basic routing
        print("Adding routing...")
        routing = PCBRouting(board)

        # Route from resistor to LED
        routing.add_trace(
            start_x=-8,  # Near resistor pin 2
            start_y=0,
            end_x=8,  # Near LED anode
            end_y=0,
            width=0.3,  # 0.3mm trace width
            layer="F.Cu",  # Front copper layer
            net_name="LED_ANODE",
        )

        # Add via for ground connection
        routing.add_via(
            x=10,  # Near LED cathode
            y=-2,
            via_type=ViaType.THROUGH,
            drill_diameter=0.2,
            pad_diameter=0.4,
            start_layer="F.Cu",
            end_layer="B.Cu",
            net_name="GND",
        )

        # Ground trace on bottom layer
        routing.add_trace(
            start_x=10,  # From via
            start_y=-2,
            end_x=0,  # To power connector
            end_y=-13,
            width=0.4,  # Wider trace for power
            layer="B.Cu",  # Back copper layer
            net_name="GND",
        )

        print("Routing completed")

        # Validate design
        print("Validating design...")
        violations = board.validate_design_rules()
        if violations:
            print("Design rule violations found:")
            for violation in violations:
                print(f"  - {violation}")
        else:
            print("No design rule violations found")

        # Get board information
        info = board.get_info()
        print("\nBoard Summary:")
        print(f"  Name: {info.get('name', 'Unknown')}")
        print(f"  Components: {info.get('component_count', 0)}")
        print(f"  Nets: {info.get('net_count', 0)}")
        print(f"  Layers: {info.get('layer_count', 0)}")

        return board

    except Exception as e:
        print(f"Error creating PCB: {str(e)}")
        return None


def save_pcb_example(board: PCBBoard, output_dir: str = "./output"):
    """
    Save the PCB and export manufacturing files.

    Args:
        board: PCB board to save
        output_dir: Output directory for files
    """

    if board is None:
        print("No board to save")
        return

    try:
        import os

        os.makedirs(output_dir, exist_ok=True)

        # Save KiCad board file
        board_file = os.path.join(output_dir, f"{board.name}.kicad_pcb")
        board.save(board_file)
        print(f"Board saved to: {board_file}")

        # Export manufacturing files
        exporter = PCBExport(board)

        # Export Gerber files
        gerber_dir = os.path.join(output_dir, "gerbers")
        gerber_files = exporter.export_gerbers(gerber_dir)
        print(f"Exported {len(gerber_files)} Gerber files")

        # Export drill files
        drill_dir = os.path.join(output_dir, "drill")
        drill_files = exporter.export_drill_files(drill_dir)
        print(f"Exported {len(drill_files)} drill files")

        # Export pick and place
        pnp_file = os.path.join(output_dir, "assembly.csv")
        exporter.export_pick_and_place(pnp_file)
        print(f"Pick and place file: {pnp_file}")

        # Export BOM
        bom_file = os.path.join(output_dir, "bom.csv")
        exporter.export_bill_of_materials(bom_file)
        print(f"BOM file: {bom_file}")

        print(f"All files exported to: {output_dir}")

    except Exception as e:
        print(f"Error saving PCB: {str(e)}")


if __name__ == "__main__":
    # Run the example
    print("=== Basic PCB Creation Example ===")
    board = basic_pcb_example()

    if board:
        print("\n=== Saving PCB Files ===")
        save_pcb_example(board)

        print("\n=== Example Complete ===")
        print("Check the ./output directory for generated files")
    else:
        print("Example failed - check KiCad installation")
