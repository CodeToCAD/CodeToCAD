"""An LED driver: schematic capture AND the physical board, from one circuit.

A battery drives an LED through a 150 ohm resistor. The circuit exports a
KiCad netlist (led_board.net) and schematic SVG (led_board.svg); because
every component carries a footprint with a placeholder 3D body, the same
component objects are Part3Ds that get placed onto a PCB Part3D assembly
and exported as STLs (led_board_stl/). With the open3d extra installed the
board is also rendered to led_board_3d.png.

Requires the skidl extra and netlistsvg (see the examples README).
Run:  python led_board.py
"""

from pathlib import Path

from codetocad import (
    Circuit,
    Footprint,
    Location,
    MaterialBase,
    Vec4,
    cube,
    led,
    resistor,
    voltage_source,
)
from codetocad_integrations.skidl import export_netlist, export_schematic

BOARD_LENGTH, BOARD_WIDTH, BOARD_HEIGHT = "50mm", "24mm", "1.6mm"

# A compact 2-pin power header for the supply, instead of the default
# (large) AA battery holder, so it sits neatly on this small board.
POWER_HEADER = Footprint(
    "Connector_PinHeader_2.54mm:PinHeader_1x02_P2.54mm_Vertical",
    body="box",
    length="6mm",
    width="5mm",
    height="8mm",
)


def build_circuit() -> Circuit:
    circuit = Circuit("led_board")
    battery = circuit.add(voltage_source(dc=5, footprint=POWER_HEADER))
    r1 = circuit.add(resistor(150))
    d1 = circuit.add(led())
    circuit.connect(battery["+"], r1[1], name="VCC")
    circuit.connect(r1[2], d1["A"], name="VLED")
    circuit.connect(d1["K"], battery["-"], circuit.gnd)
    return circuit


def build_board(circuit: Circuit):
    """Place each component's footprint body on a PCB blank."""
    board = cube(BOARD_LENGTH, BOARD_WIDTH, BOARD_HEIGHT)
    board.name = "pcb"
    board.set_material(MaterialBase("fr4", color_rgba=Vec4(0.1, 0.45, 0.2, 1.0)))

    # Stand each part on the board top (parts are centered on their origin),
    # spread left-to-right: supply header, series resistor, then the LED.
    positions = {"V1": -0.017, "R1": 0.0, "D1": 0.017}
    for component in circuit.components:
        half_body = (component.footprint.height or 0) / 2
        component.transform(
            absolute=Location(x=positions[component.reference], z=0.0008 + half_body)
        )
    return board, circuit.components


def main() -> None:
    circuit = build_circuit()
    assert circuit.validate() == []
    export_netlist(circuit, "led_board.net")
    export_schematic(circuit, "led_board.svg")

    board, components = build_board(circuit)
    stl_dir = Path("led_board_stl")
    stl_dir.mkdir(exist_ok=True)
    for part in (board, *components):
        label = getattr(part, "reference", None) or part.name
        part.export(str(stl_dir / f"{label}.stl"))
    print(f"wrote led_board.net, led_board.svg and {stl_dir}/*.stl")

    try:
        from codetocad_integrations.open3d import render
    except ImportError:
        print("install the open3d extra to render led_board_3d.png")
        return
    render(
        board,
        *components,
        path="led_board_3d.png",
        front=(-0.3, -0.8, 0.6),
        zoom=0.9,
    )
    print("wrote led_board_3d.png")


if __name__ == "__main__":
    main()
