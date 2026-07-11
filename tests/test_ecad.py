import pytest

from codetocad import (
    Circuit,
    CommonFootprints,
    ComponentType,
    Footprint,
    Part3D,
    capacitor,
    current_source,
    diode,
    format_si,
    inductor,
    led,
    parse_si,
    resistor,
    voltage_source,
)


# -- SI values --


@pytest.mark.parametrize(
    "text,expected",
    [
        ("10k", 10_000),
        ("100n", 1e-7),
        ("2.2meg", 2.2e6),
        ("3m", 3e-3),
        ("4.7uF", 4.7e-6),  # trailing unit letters after the suffix ignored
        ("470", 470),
        (1000, 1000.0),
    ],
)
def test_parse_si(text, expected):
    assert parse_si(text) == pytest.approx(expected)


@pytest.mark.parametrize(
    "value,expected", [(10_000, "10k"), (4.7e-6, "4.7u"), (1e6, "1meg"), (0, "0")]
)
def test_format_si(value, expected):
    assert format_si(value) == expected


# -- components --


def test_components_have_pins_values_and_footprints():
    r = resistor("10k")
    assert r.component_type is ComponentType.RESISTOR
    assert r.resistance == 10_000
    assert r.value == "10k"
    assert [p.name for p in r.pins] == ["1", "2"]
    assert r.footprint.library_id.startswith("Resistor_THT")
    assert r.get_volume() > 0  # the footprint gives it a real 3D body

    d = led()
    assert d.component_type is ComponentType.LED
    assert d["A"].name == "A" and d[2].name == "K"
    assert d["k"].name == "K"  # case-insensitive lookup
    with pytest.raises(KeyError):
        d["Z"]


def test_source_waveform_and_dc():
    v = voltage_source(dc=5)
    assert v.dc == 5 and v.value == "5V"
    pulse = voltage_source(waveform="PULSE(0 5 0 1u 1u 1m 2m)")
    assert pulse.waveform.startswith("PULSE")
    i = current_source(dc=0.001)
    assert i.component_type is ComponentType.CURRENT_SOURCE


def test_component_is_a_part3d():
    assert isinstance(resistor(100), Part3D)


def test_other_two_terminals():
    assert capacitor("100n").capacitance == pytest.approx(1e-7)
    assert inductor("10m").inductance == pytest.approx(1e-2)
    assert diode().component_type is ComponentType.DIODE
    assert [p.name for p in diode().pins] == ["A", "K"]


# -- footprints --


def test_footprint_makes_bodies():
    fp = CommonFootprints.axial_resistor.footprint()
    assert isinstance(fp, Footprint)
    part3d = fp.to_part3d()
    assert part3d.get_volume() > 0
    part2d = fp.to_part2d()
    assert part2d.get_area() > 0


# -- circuit connectivity --


def _divider():
    circuit = Circuit("divider")
    v1 = circuit.add(voltage_source(dc=9))
    r1, r2 = circuit.add(resistor("10k"), resistor("20k"))
    circuit.connect(v1["+"], r1[1], name="VIN")
    circuit.connect(r1[2], r2[1], name="VOUT")
    circuit.connect(r2[2], v1["-"], circuit.gnd)
    return circuit, v1, r1, r2


def test_reference_designators_assigned():
    circuit, v1, r1, r2 = _divider()
    assert (v1.reference, r1.reference, r2.reference) == ("V1", "R1", "R2")
    assert circuit.get_component("R2") is r2


def test_nets_merge_and_carry_pins():
    circuit, v1, r1, r2 = _divider()
    vout = circuit.get_net("VOUT")
    assert set(vout.pins) == {r1[2], r2[1]}
    assert r1[2].net is vout
    # The ground net collects both the R2 bottom and the source return.
    assert circuit.gnd.is_ground
    assert set(circuit.gnd.pins) == {r2[2], v1["-"]}


def test_connect_reuses_named_net():
    circuit = Circuit()
    r1, r2 = circuit.add(resistor(1), resistor(2))
    a = circuit.connect(r1[1], name="A")
    b = circuit.connect(r2[1], name="A")
    assert a is b and len(a.pins) == 2


def test_validate_flags_floating_and_missing_ground():
    circuit = Circuit()
    r1 = circuit.add(resistor(1))
    circuit.connect(r1[1], r1[2])  # a loop with no ground
    warnings = circuit.validate()
    assert any("ground" in w for w in warnings)

    circuit2, *_ = _divider()
    assert circuit2.validate() == []


def test_connect_rejects_raw_component():
    circuit = Circuit()
    r1 = resistor(1)
    with pytest.raises(TypeError):
        circuit.connect(r1)  # must pass a Pin, e.g. r1[1]
