"""Render CodeToCAD Circuits as schematic SVGs.

Uses `netlistsvg <https://github.com/nturley/netlistsvg>`_ (the same
rendering engine skidl's ``generate_svg`` shells out to) with its analog
skin, so components are drawn with standard schematic symbols (resistor,
capacitor, LED, sources, ground, ...) and the layout is computed
automatically by ELK.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import tempfile
from pathlib import Path

from codetocad.ecad import Circuit, ComponentType, Net


def find_netlistsvg() -> str:
    """Locate the netlistsvg executable."""
    override = os.environ.get("CODETOCAD_NETLISTSVG")
    if override:
        return override
    found = shutil.which("netlistsvg")
    if found:
        return found
    home_install = (
        Path.home() / ".codetocad" / "netlistsvg" / "node_modules" / ".bin" / "netlistsvg"
    )
    if home_install.exists():
        return str(home_install)
    raise FileNotFoundError(
        "netlistsvg not found. Install it with `npm install -g netlistsvg` "
        "(requires Node.js), or into the home dir with `npm install --prefix "
        "~/.codetocad/netlistsvg netlistsvg`, or set CODETOCAD_NETLISTSVG to "
        "the executable."
    )


def _find_analog_skin(netlistsvg_path: str) -> Path:
    """The analog skin ships inside the netlistsvg package; resolve the bin
    symlink to find it."""
    override = os.environ.get("CODETOCAD_NETLISTSVG_SKIN")
    if override:
        return Path(override)
    script = Path(netlistsvg_path).resolve()  # .../netlistsvg/bin/netlistsvg.js
    for package_root in (script.parent.parent, *script.parents):
        skin = package_root / "lib" / "analog.svg"
        if skin.exists():
            return skin
    raise FileNotFoundError(
        f"netlistsvg's analog skin was not found near {netlistsvg_path}; "
        "reinstall netlistsvg or set CODETOCAD_NETLISTSVG_SKIN to analog.svg"
    )


# (horizontal, vertical) netlistsvg analog-skin cell types per component.
_SKIN_TYPES = {
    ComponentType.RESISTOR: ("r_h", "r_v"),
    ComponentType.CAPACITOR: ("c_h", "c_v"),
    ComponentType.INDUCTOR: ("l_h", "l_v"),
    ComponentType.DIODE: ("d_h", "d_v"),
    ComponentType.LED: ("d_led_h", "d_led_v"),
    ComponentType.VOLTAGE_SOURCE: ("v", "v"),
    ComponentType.CURRENT_SOURCE: ("i", "i"),
    ComponentType.TRANSISTOR_NPN: ("q_npn", "q_npn"),
    ComponentType.TRANSISTOR_PNP: ("q_pnp", "q_pnp"),
}

# Skin port names (and layout direction) for the pins, in pin order.
_TWO_TERMINAL_PORTS = (("A", "input"), ("B", "output"))
_POLARIZED_PORTS = (("+", "input"), ("-", "output"))
_SOURCE_PORTS = (("+", "output"), ("-", "input"))


def _component_ports(component) -> tuple[tuple[str, str], ...]:
    kind = component.component_type
    if kind in (ComponentType.DIODE, ComponentType.LED):
        return _POLARIZED_PORTS
    if kind in (ComponentType.VOLTAGE_SOURCE, ComponentType.CURRENT_SOURCE):
        return _SOURCE_PORTS
    if kind in (ComponentType.TRANSISTOR_NPN, ComponentType.TRANSISTOR_PNP):
        return (("C", "input"), ("B", "input"), ("E", "output"))
    return _TWO_TERMINAL_PORTS


def _is_signal_label(net: Net) -> bool:
    """Named nets get a flag symbol; auto-named (N1, N2, ...) don't."""
    return not net._auto_named and not net.is_ground and not net.is_power


def to_netlistsvg_json(circuit: Circuit) -> dict:
    """Build the netlistsvg (yosys-style) JSON description of ``circuit``,
    mapping components onto the analog skin's symbols."""
    net_numbers = {id(net): number for number, net in enumerate(circuit.nets, 2)}
    cells: dict[str, dict] = {}

    def add_cell(key, cell_type, connections, directions, attributes=None):
        # netlistsvg (yosys convention) splits cell names on ".", so the key
        # must be period-free; the human labels ride in ``attributes``
        # (rendered in the skin's "ref"/"value" text slots).
        cell = {
            "type": cell_type,
            "port_directions": directions,
            "connections": connections,
        }
        if attributes:
            cell["attributes"] = attributes
        cells[key] = cell

    for component in circuit.components:
        connected = [pin for pin in component.pins if pin.net is not None]
        if not connected:
            continue
        reference = component.reference or component.name or f"U{len(cells)}"
        attributes = {"ref": reference}
        if component.value:
            attributes["value"] = component.value
        kind = component.component_type
        if kind in _SKIN_TYPES:
            ports = _component_ports(component)
            # Components hanging off a ground/power rail read better drawn
            # vertically, like the rail itself.
            vertical = any(
                pin.net.is_ground or pin.net.is_power for pin in connected
            )
            cell_type = _SKIN_TYPES[kind][1 if vertical else 0]
            connections = {}
            directions = {}
            for pin, (port, direction) in zip(component.pins, ports):
                if pin.net is None:
                    continue
                connections[port] = [net_numbers[id(pin.net)]]
                directions[port] = direction
        else:
            # Generic box with one port per pin.
            cell_type = component.name or kind.value
            connections = {}
            directions = {}
            for pin in connected:
                connections[pin.name] = [net_numbers[id(pin.net)]]
                directions[pin.name] = (
                    "output" if pin.pin_type.value in ("output", "power_out") else "input"
                )
        add_cell(reference, cell_type, connections, directions, attributes)

    for net in circuit.nets:
        number = net_numbers[id(net)]
        if not net.pins:
            continue
        if net.is_ground:
            add_cell(f"gnd_{net.name}", "gnd", {"A": [number]}, {"A": "input"})
        elif net.is_power:
            add_cell(
                f"vcc_{net.name}",
                "vcc",
                {"A": [number]},
                {"A": "output"},
                {"name": net.name},
            )
        elif _is_signal_label(net):
            name = (net.name or "").upper()
            if name.startswith(("VIN", "IN")):
                add_cell(net.name, "$_inputExt_", {"Y": [number]}, {"Y": "output"})
            else:
                add_cell(net.name, "$_outputExt_", {"A": [number]}, {"A": "input"})

    return {"modules": {circuit.name: {"ports": {}, "cells": cells}}}


def export_schematic(
    circuit: Circuit,
    path: str,
    *,
    netlistsvg_path: str | None = None,
    skin: str | None = None,
    timeout: float = 120.0,
) -> str:
    """Render ``circuit`` to a schematic SVG at ``path`` with netlistsvg's
    analog symbol skin. Returns ``path``."""
    netlistsvg = netlistsvg_path or find_netlistsvg()
    skin_path = Path(skin) if skin else _find_analog_skin(netlistsvg)
    schematic = to_netlistsvg_json(circuit)
    with tempfile.TemporaryDirectory(prefix="codetocad_schematic_") as tmp:
        json_path = Path(tmp) / f"{circuit.name}.json"
        json_path.write_text(json.dumps(schematic, indent=2))
        result = subprocess.run(
            [netlistsvg, str(json_path), "--skin", str(skin_path), "-o", str(path)],
            capture_output=True,
            text=True,
            timeout=timeout,
        )
    if result.returncode != 0 or not Path(path).exists():
        raise RuntimeError(
            f"netlistsvg failed (exit {result.returncode}):\n{result.stderr}"
        )
    return path
