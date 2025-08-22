#!/usr/bin/env python3
"""
Example demonstrating KiCad adapter with kipy (kicad-python).

This example shows how the CodeToCAD KiCad adapter works with kipy/kicad-python.

Usage:
    python kipy_example.py
"""


def main():
    """Demonstrate KiCad kipy usage."""
    print("=== KiCad kipy Example ===")

    # Check kipy availability
    try:
        from kipy import KiCad

        print("✅ kipy (kicad-python) is available")
    except ImportError:
        try:
            from kicad import KiCad

            print("✅ kicad-python is available")
        except ImportError:
            print("❌ Neither kipy nor kicad-python is available")
            print("Please install with: pip install kicad-python")
            return

    # Example using CodeToCAD's PCB interface
    try:
        from codetocad.adapters.kicad.pcb.pcb_board import PCBBoard
        from codetocad.interfaces.cad.pcb.pcb_board_interface import BoardDimensions

        print("\n🎯 Creating PCB board with CodeToCAD interface:")

        # Create board
        board = PCBBoard()
        dimensions = BoardDimensions(width=50.0, height=40.0)

        # This will use kipy automatically
        board.create_board("example_board", dimensions)
        print("  ✅ Board created successfully")

        # Add components using presets
        from codetocad.interfaces.cad.pcb.component_presets.resistor_presets import (
            ResistorPresets,
        )

        resistor_presets = ResistorPresets()
        resistor = resistor_presets.smd_0603("10k", tolerance="1%")
        print(f"  ✅ Created resistor preset: {resistor.reference_designator}")

    except Exception as e:
        print(f"  ❌ CodeToCAD PCB interface failed: {e}")

    print("\n=== Summary ===")
    print("✅ Using kipy/kicad-python as the only KiCad API")
    print("   - Requires KiCad 9.0+ running with API enabled")
    print("   - Modern approach for KiCad integration")
    print("   - Install with: pip install kicad-python")


if __name__ == "__main__":
    main()
