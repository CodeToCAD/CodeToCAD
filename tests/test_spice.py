import numpy as np
import pytest

from codetocad import Circuit, capacitor, led, resistor, voltage_source
from codetocad_integrations.spice import to_netlist


def _divider(dc=9):
    circuit = Circuit("divider")
    v1 = circuit.add(voltage_source(dc=dc))
    r1, r2 = circuit.add(resistor("10k"), resistor("20k"))
    circuit.connect(v1["+"], r1[1], name="VIN")
    circuit.connect(r1[2], r2[1], name="VOUT")
    circuit.connect(r2[2], v1["-"], circuit.gnd)
    return circuit, v1


# -- netlist generation (no simulator needed) --


def test_netlist_maps_primitives_and_ground():
    circuit, _ = _divider()
    netlist = to_netlist(circuit)
    assert "R1 VIN VOUT 10k" in netlist
    assert "R2 VOUT 0 20k" in netlist  # ground net is node 0
    assert "V1 VIN 0 DC 9" in netlist
    assert netlist.strip().endswith(".end")


def test_netlist_derives_led_diode_model():
    circuit = Circuit("led")
    v1 = circuit.add(voltage_source(dc=5))
    r1 = circuit.add(resistor(150))
    d1 = circuit.add(led())
    circuit.connect(v1["+"], r1[1], name="VCC")
    circuit.connect(r1[2], d1["A"], name="VLED")
    circuit.connect(d1["K"], v1["-"], circuit.gnd)
    netlist = to_netlist(circuit)
    assert "D1 VLED 0 D_D1" in netlist
    assert ".model D_D1 D(" in netlist


def test_netlist_rejects_unconnected_pins():
    circuit = Circuit()
    r1 = circuit.add(resistor(1))
    circuit.connect(r1[1], circuit.gnd)
    with pytest.raises(ValueError, match="unconnected"):
        to_netlist(circuit)


# -- end-to-end with ngspice (skipped when unavailable) --


def _ngspice_available():
    try:
        from codetocad_integrations.spice import find_ngspice

        find_ngspice()
        return True
    except FileNotFoundError:
        return False


ngspice = pytest.mark.skipif(not _ngspice_available(), reason="ngspice not installed")


@ngspice
def test_operating_point_divider(tmp_path):
    from codetocad_integrations.spice import simulate

    circuit, v1 = _divider(dc=9)
    op = simulate(circuit, output_dir=tmp_path).operating_point()
    assert op.voltage("VOUT") == pytest.approx(6.0, abs=1e-6)
    assert op.voltage("VIN") == pytest.approx(9.0, abs=1e-6)
    # 9V across 30k -> 0.3mA; branch current is into V1's + terminal.
    assert op.current(v1) == pytest.approx(-0.3e-3, rel=1e-3)


@ngspice
def test_dc_sweep(tmp_path):
    from codetocad_integrations.spice import simulate

    circuit, v1 = _divider(dc=9)
    sweep = simulate(circuit, output_dir=tmp_path).dc_sweep(v1, 0, 9, 1)
    assert sweep.sweep[0] == pytest.approx(0.0)
    assert sweep.sweep[-1] == pytest.approx(9.0)
    # VOUT tracks 2/3 of the swept supply.
    assert np.allclose(np.real(sweep["VOUT"]), 2 / 3 * sweep.sweep, atol=1e-6)


@ngspice
def test_rc_lowpass_ac_corner(tmp_path):
    import math

    from codetocad_integrations.spice import simulate

    resistance, capacitance = 1600.0, 100e-9
    circuit = Circuit("rc")
    v1 = circuit.add(voltage_source(ac=1))
    r1 = circuit.add(resistor(resistance))
    c1 = circuit.add(capacitor(capacitance))
    circuit.connect(v1["+"], r1[1], name="VIN")
    circuit.connect(r1[2], c1[1], name="VOUT")
    circuit.connect(c1[2], v1["-"], circuit.gnd)

    ac = simulate(circuit, output_dir=tmp_path).ac(10, "1meg", points_per_decade=30)
    corner = ac.frequency[np.argmin(np.abs(ac.magnitude_db("VOUT") + 3.0))]
    analytic = 1 / (2 * math.pi * resistance * capacitance)
    assert corner == pytest.approx(analytic, rel=0.05)


@ngspice
def test_transient_rc_charge(tmp_path):
    from codetocad_integrations.spice import simulate

    circuit = Circuit("rc_step")
    v1 = circuit.add(voltage_source(waveform="PULSE(0 1 0 1u 1u 1 2)"))
    r1 = circuit.add(resistor(1000))
    c1 = circuit.add(capacitor(1e-6))  # tau = 1 ms
    circuit.connect(v1["+"], r1[1], name="VIN")
    circuit.connect(r1[2], c1[1], name="VOUT")
    circuit.connect(c1[2], v1["-"], circuit.gnd)

    tran = simulate(circuit, output_dir=tmp_path).transient("10u", "5m")
    vout = np.real(tran["VOUT"])
    # After ~1 tau (1ms) an RC step reaches ~63%.
    near_tau = np.argmin(np.abs(tran.time - 1e-3))
    assert vout[near_tau] == pytest.approx(0.632, abs=0.03)
    assert vout[-1] == pytest.approx(1.0, abs=0.02)  # fully charged by 5ms
