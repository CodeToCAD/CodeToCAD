"""The actuator / sensor catalog: every factory builds a valid Part3D with
real dimensions, a moving element where applicable, and power specs; the
motor-control mixins and registry helpers work."""

import math

import pytest

import codetocad_integrations.library as lib
from codetocad.joints import PrismaticJoint, RevoluteJoint
from codetocad.mixins import (
    BLDCMotorMixin,
    CameraMixin,
    DCMotorMixin,
    EncoderMixin,
    IMUMixin,
    StepperMotorMixin,
)
from codetocad_integrations.library._base import CATALOG

_ROTARY = ("stepper", "servo", "bldc", "dc_gearmotor")


def test_catalog_has_at_least_100_actuators():
    actuators = [
        e for e in CATALOG.values()
        if e.category in (*_ROTARY, "linear_actuator")
    ]
    assert len(actuators) >= 100


@pytest.mark.parametrize("slug", sorted(CATALOG))
def test_every_part_builds(slug):
    """Each factory returns a Part3D with a non-degenerate bounding box and
    a (possibly empty) power spec, and never raises."""
    part = CATALOG[slug].factory()
    bbox_min, bbox_max = part.get_bounding_box()
    for lo, hi in zip(bbox_min.to_tuple(), bbox_max.to_tuple()):
        assert hi > lo
    assert isinstance(part.get_power_requirements(), dict)
    assert part.describe()


@pytest.mark.parametrize(
    "slug", sorted(s for s, e in CATALOG.items() if e.category in _ROTARY)
)
def test_rotary_actuators_have_a_hinged_shaft(slug):
    part = CATALOG[slug].factory()
    assert isinstance(part.shaft_joint, RevoluteJoint)
    assert part.shaft.name == f"{slug}_shaft"


def test_get_nema_23_headline():
    motor = lib.get_nema_23()
    assert isinstance(motor, StepperMotorMixin)
    assert motor.power.holding_torque_nm == pytest.approx(1.26)
    # frame is the 57 mm NEMA 23 square
    bbox_min, bbox_max = motor.get_bounding_box()
    assert (bbox_max.x - bbox_min.x) == pytest.approx(0.057, abs=1e-6)
    # driving it records the command a bound microcontroller would send
    motor.set_velocity(120)
    assert motor.get_last_command() == {"velocity_rpm": 120.0}
    motor.move_steps(200)
    assert motor.get_last_command() == {"steps": 200}


def test_get_by_slug_matches_named_factory():
    assert lib.get("nema_23").part_number == lib.get_nema_23().part_number
    with pytest.raises(KeyError):
        lib.get("does_not_exist")


def test_servo_angle_and_continuous_rotation():
    servo = lib.get_mg996r()
    servo.set_angle(90)
    assert servo.get_last_command() == {"angle_degrees": 90.0}
    servo.set_angle(500)  # clamped to the 180 deg travel
    assert servo.get_angle() == 180.0

    cont = lib.get_fs90r()
    assert cont.continuous
    with pytest.raises(ValueError):
        cont.set_angle(90)
    cont.set_speed(0.5)
    assert cont.get_last_command() == {"speed": 0.5}


def test_bldc_speed_scales_with_kv():
    motor = lib.get_drone_2205_2300kv()
    assert isinstance(motor, BLDCMotorMixin)
    power = motor.get_power_requirements()
    assert power["no_load_speed_rpm"] == pytest.approx(
        power["kv_rpm_per_v"] * power["nominal_voltage_v"]
    )


def test_linear_actuator_rod_slides():
    act = lib.get_actuonix_l16_100()
    assert isinstance(act.rod_joint, PrismaticJoint)
    act.extend()
    assert act.get_last_command() == {"stroke_mm": 100.0}
    act.retract()
    assert act.get_last_command() == {"stroke_mm": 0.0}
    act.set_stroke(999)  # clamped to stroke length
    assert act._target_stroke_mm == 100.0


def test_sensor_mixins_are_wired():
    assert isinstance(lib.get_rpi_camera_v2(), CameraMixin)
    assert isinstance(lib.get_mpu6050(), IMUMixin)
    assert isinstance(lib.get_as5600(), EncoderMixin)
    assert lib.get_qtr_8rc().channels == 8
    assert lib.get_vl53l0x().max_range_m == 2.0
    assert lib.get_microswitch_limit().is_active() is False  # no reading yet


def test_dc_gearmotor_is_dc_motor():
    motor = lib.get_tt_gearmotor()
    assert isinstance(motor, DCMotorMixin)
    assert motor.no_load_speed_rpm == 200
    assert motor.set_speed(50) is motor  # DCMotorMixin alias
    assert motor.get_last_command() == {"velocity_rpm": 50.0}


def test_transmission_travel_math():
    screw = lib.get_leadscrew_t8_2mm()
    assert screw.linear_travel(10) == pytest.approx(20.0)
    assert screw.revolutions_for(20.0) == pytest.approx(10.0)

    capstan = lib.get_capstan_drum_20mm()
    assert capstan.travel_per_rev_mm == pytest.approx(math.pi * 20, abs=1e-2)

    pulley = lib.get_gt2_pulley_20t()
    assert pulley.travel_per_rev_mm == pytest.approx(40.0)  # 20 teeth * 2 mm


def test_spur_gear_generator_and_mesh_math():
    from codetocad_integrations.library.gears import spur_gear

    pinion = spur_gear(module_mm=1.0, teeth=20)
    wheel = spur_gear(module_mm=1.0, teeth=60)
    assert pinion.pitch_diameter_mm == 20.0
    assert pinion.outer_diameter_mm == 22.0  # module * (teeth + 2)
    assert pinion.ratio_with(wheel) == pytest.approx(3.0)
    assert pinion.center_distance_to(wheel) == pytest.approx(40.0)
    # a registered preset resolves the same way
    assert lib.get_spur_gear_m1_20t().pitch_diameter_mm == 20.0


def test_worm_and_rack_ratios():
    worm = lib.get_worm_m2_2start()
    wheel = lib.get_spur_gear_m2_40t()
    assert worm.ratio_with(wheel) == pytest.approx(20.0)  # 40 teeth / 2 starts
    rack = lib.get_gear_rack_m2_500mm()
    pinion = lib.get_spur_gear_m2_20t()
    assert rack.travel_per_pinion_rev_mm(pinion) == pytest.approx(
        math.pi * pinion.pitch_diameter_mm
    )


def test_universal_joint_articulates():
    from codetocad.joints import RevoluteJoint
    from codetocad.simulation import extract_links

    uj = lib.get_universal_joint_8mm()
    assert isinstance(uj.bend_joint, RevoluteJoint)
    joint_types = {
        link.joint.joint_type for link in extract_links(uj) if link.joint
    }
    assert {"fixed", "revolute"} <= joint_types  # cross welded, output bends


def test_coupling_and_bearing_specs():
    cp = lib.get_coupling_5x8_jaw()
    assert (cp.bore_a_mm, cp.bore_b_mm, cp.coupling_type) == (5, 8, "jaw")
    b608 = lib.get_bearing_608()
    assert (b608.bore_mm, b608.outer_diameter_mm, b608.width_mm) == (8, 22, 7)
    lm8 = lib.get_lm8uu()
    assert lm8.bore_mm == 8 and lm8.kind == "linear ball bushing"


def test_fasteners_bridge_and_clearance_hole():
    from codetocad import CommonFasteners
    from codetocad_integrations.library.fasteners import from_common

    bolt = lib.get_m3x12_socket_head()
    assert bolt.thread_mm == 3 and bolt.length_mm == 12
    assert bolt.clearance_hole_mm == 3.4  # ISO medium fit for M3
    # the core enum is bridged, not moved: it still lives in codetocad
    wrapped = from_common(CommonFasteners.M3_BOLT)
    assert wrapped.thread_mm == 3 and wrapped.kind == "bolt"


def test_power_and_driver_specs():
    pack = lib.get_lipo_3s_2200()
    assert pack.capacity_mah == 2200 and pack.cells == 3
    assert pack.get_power_requirements()["nominal_voltage_v"] == 11.1
    driver = lib.get_a4988()
    assert driver.max_current_a == 2.0 and driver.interface == "STEP/DIR"


def test_board_and_wheel_helpers():
    pico = lib.get_rpi_pico()
    assert pico.chip == "RP2040" and pico.logic_voltage == 3.3
    wheel = lib.get_tt_wheel_65mm()
    assert wheel.distance_per_rev_mm() == pytest.approx(math.pi * 65)


def test_structure_generators():
    from codetocad_integrations.library.structure import extrusion, smooth_rod

    ext = extrusion(20, 500, width_mm=40)
    lo, hi = ext.get_bounding_box()
    assert (hi.x - lo.x) == pytest.approx(0.5)  # 500 mm long
    assert ext.profile == "2040"
    rod = smooth_rod(8, 300)
    assert rod.diameter_mm == 8 and rod.length_mm == 300


def test_gripper_jaw_moves():
    from codetocad.joints import PrismaticJoint

    gripper = lib.get_parallel_gripper_servo()
    assert isinstance(gripper.jaw_joint, PrismaticJoint)
    gripper.open()
    assert gripper.get_last_command() == {"opening_mm": 35.0}
    gripper.close()
    assert gripper.get_last_command() == {"opening_mm": 0.0}


def test_registry_helpers():
    assert "nema_23" in lib.list_parts("stepper")
    assert set(lib.categories()) >= {"stepper", "servo", "bldc", "camera",
                                     "bolt", "battery", "sbc", "gripper"}
    assert "gimbal_gm2804" in lib.search("gimbal")
    assert "m3x12_socket_head" in lib.search("socket")


def test_export_includes_shaft(tmp_path):
    """Exporting a motor writes the body *and* its shaft (assembly)."""
    motor = lib.get_nema_17()
    out = motor.export(str(tmp_path / "nema17.stl"))
    text = open(out).read()
    # body cube (12 facets) plus a shaft cylinder -> well over 12 facets
    assert text.count("facet normal") > 20
