"""Convert CodeToCAD Circuits to skidl and export netlists/ERC."""

from __future__ import annotations

from pathlib import Path

import skidl as _skidl
from skidl.pin import pin_drives, pin_types

from codetocad.ecad import Circuit, PinType

_PIN_FUNCS = {
    PinType.PASSIVE: pin_types.PASSIVE,
    PinType.INPUT: pin_types.INPUT,
    PinType.OUTPUT: pin_types.OUTPUT,
    PinType.BIDIRECTIONAL: pin_types.BIDIR,
    PinType.POWER_IN: pin_types.PWRIN,
    PinType.POWER_OUT: pin_types.PWROUT,
    PinType.NO_CONNECT: pin_types.NOCONNECT,
}


def to_skidl(circuit: Circuit) -> "_skidl.Circuit":
    """Build a skidl ``Circuit`` mirroring ``circuit``: one skidl Part per
    component (with reference, value and footprint) and one skidl Net per
    net."""
    sk_circuit = _skidl.Circuit(name=circuit.name)

    sk_nets = {}
    for net in circuit.nets:
        sk_net = _skidl.Net(net.name, circuit=sk_circuit)
        if net.is_ground or net.is_power:
            # Ground/power rails are driven by the supply, not a pin.
            sk_net.drive = pin_drives.POWER
        sk_nets[id(net)] = sk_net

    for component in circuit.components:
        pins = [
            _skidl.Pin(
                num=pin.number,
                name=pin.name,
                func=_PIN_FUNCS.get(pin.pin_type, pin_types.PASSIVE),
            )
            for pin in component.pins
        ]
        part = _skidl.Part(
            name=component.name or component.component_type.value,
            tool=_skidl.SKIDL,
            ref_prefix=component.component_type.ref_prefix,
            circuit=sk_circuit,
            pins=pins,
        )
        if component.reference:
            part.ref = component.reference
        part.value = component.value or ""
        if component.description:
            part.description = component.description
        if component.footprint is not None:
            part.footprint = component.footprint.library_id
        for pin in component.pins:
            if pin.net is not None:
                sk_nets[id(pin.net)] += part[pin.number]

    return sk_circuit


def export_netlist(circuit: Circuit, path: str | None = None) -> str:
    """Generate a KiCad netlist with skidl; optionally write it to
    ``path`` (conventionally ``.net``). Returns the netlist text."""
    text = str(to_skidl(circuit).generate_netlist())
    if path is not None:
        Path(path).write_text(text)
    return text


def export_xml(circuit: Circuit, path: str | None = None) -> str:
    """Generate the netlist as KiCad XML (for BOM tools); optionally write
    it to ``path``. Returns the XML text."""
    text = str(to_skidl(circuit).generate_xml())
    if path is not None:
        Path(path).write_text(text)
    return text


def erc(circuit: Circuit) -> None:
    """Run skidl's electrical rules check; findings are logged to the
    console and the ``.erc`` file skidl writes in the working directory."""
    to_skidl(circuit).ERC()
