"""Compute boards: microcontroller dev boards (Arduino, RP2040, ESP32,
Teensy, STM32 ...) and single-board computers (Raspberry Pi, Jetson,
BeagleBone). These are the *physical board outlines* -- for the logical
pin-binding API use :class:`codetocad.Microcontroller` (see
``.agents/integrations/controls.md``); mount that logic on one of these
footprints for layout.

Each returns a ``Part3D`` at real PCB dimensions with ``chip``,
``logic_voltage``, ``gpio`` and ``connectivity`` attributes.
"""

from __future__ import annotations

from ._base import PCB_GREEN, BODY_BLACK, PassivePart, PowerSpec, register


class ControllerBoard(PassivePart):
    category = "board"


# slug, category, (l,w,h), mass, color, chip, logic_V, current_A, power_W,
# gpio, connectivity, mfr, pn, notes
_ITEMS = [
    # --- microcontroller boards ---
    ("arduino_uno", "microcontroller_board", (68.6, 53.4, 15), 0.025, PCB_GREEN,
     "ATmega328P", 5.0, 0.05, 0.25, 20, "USB", "Arduino", "Uno R3",
     "the classic 8-bit Arduino"),
    ("arduino_nano", "microcontroller_board", (45, 18, 7), 0.007, PCB_GREEN,
     "ATmega328P", 5.0, 0.02, 0.1, 22, "USB", "Arduino", "Nano",
     "breadboard-friendly ATmega328"),
    ("arduino_mega", "microcontroller_board", (101.5, 53.3, 15), 0.037, PCB_GREEN,
     "ATmega2560", 5.0, 0.08, 0.4, 54, "USB", "Arduino", "Mega 2560",
     "high pin-count 8-bit board (RepRap classic)"),
    ("rpi_pico", "microcontroller_board", (51, 21, 4), 0.003, BODY_BLACK,
     "RP2040", 3.3, 0.03, 0.1, 26, "USB", "Raspberry Pi", "Pico",
     "dual-core RP2040 board"),
    ("rpi_pico_w", "microcontroller_board", (51, 21, 4), 0.003, BODY_BLACK,
     "RP2040", 3.3, 0.05, 0.2, 26, "USB / WiFi", "Raspberry Pi", "Pico W",
     "RP2040 with WiFi"),
    ("esp32_devkit", "microcontroller_board", (55, 28, 13), 0.010, PCB_GREEN,
     "ESP32", 3.3, 0.24, 0.8, 34, "USB / WiFi / BT", "Espressif", "DevKitC",
     "WiFi + Bluetooth 32-bit board"),
    ("esp32_s3", "microcontroller_board", (63, 26, 13), 0.011, PCB_GREEN,
     "ESP32-S3", 3.3, 0.30, 1.0, 44, "USB / WiFi / BT", "Espressif", "S3 DevKit",
     "ESP32-S3 with AI acceleration"),
    ("esp8266_nodemcu", "microcontroller_board", (58, 31, 13), 0.010, PCB_GREEN,
     "ESP8266", 3.3, 0.17, 0.6, 17, "USB / WiFi", "Espressif", "NodeMCU",
     "cheap WiFi board"),
    ("teensy_40", "microcontroller_board", (35, 18, 4), 0.003, PCB_GREEN,
     "IMXRT1062", 3.3, 0.10, 0.4, 40, "USB", "PJRC", "Teensy 4.0",
     "600 MHz Cortex-M7 board (fast control loops)"),
    ("stm32_bluepill", "microcontroller_board", (53, 22, 8), 0.006, PCB_GREEN,
     "STM32F103", 3.3, 0.05, 0.2, 37, "USB", "Generic", "Blue Pill",
     "cheap 32-bit ARM board"),
    ("stm32_nucleo_f401", "microcontroller_board", (70, 82, 20), 0.030, PCB_GREEN,
     "STM32F401", 3.3, 0.10, 0.4, 50, "USB", "STMicro", "Nucleo-F401RE",
     "Nucleo dev board (Arduino headers)"),
    ("seeed_xiao_rp2040", "microcontroller_board", (20, 17.5, 3.5), 0.001, BODY_BLACK,
     "RP2040", 3.3, 0.03, 0.1, 11, "USB-C", "Seeed", "XIAO RP2040",
     "thumbnail-size RP2040 board"),
    ("teensy_lc", "microcontroller_board", (35, 18, 4), 0.002, PCB_GREEN,
     "MKL26Z64", 3.3, 0.03, 0.1, 27, "USB", "PJRC", "Teensy LC",
     "low-cost Teensy"),
    # --- single-board computers ---
    ("rpi_zero_2w", "sbc", (65, 30, 5), 0.011, PCB_GREEN,
     "RP3A0 (quad A53)", 5.0, 0.4, 2.0, 40, "WiFi / BT / USB", "Raspberry Pi",
     "Zero 2 W", "tiny quad-core Linux SBC"),
    ("rpi_4b", "sbc", (85, 56, 17), 0.046, PCB_GREEN,
     "BCM2711 (quad A72)", 5.0, 1.2, 6.0, 40, "GbE / WiFi / USB3", "Raspberry Pi",
     "4 Model B", "quad-core Linux SBC"),
    ("rpi_5", "sbc", (85, 56, 18), 0.046, PCB_GREEN,
     "BCM2712 (quad A76)", 5.0, 1.6, 8.0, 40, "GbE / WiFi / USB3 / PCIe",
     "Raspberry Pi", "5", "faster Pi with PCIe"),
    ("jetson_nano", "sbc", (100, 80, 29), 0.140, PCB_GREEN,
     "Tegra X1 (quad A57 + 128 CUDA)", 5.0, 2.0, 10.0, 40, "GbE / USB3",
     "NVIDIA", "Jetson Nano DevKit", "entry AI / vision SBC"),
    ("jetson_orin_nano", "sbc", (100, 79, 30), 0.180, PCB_GREEN,
     "Orin (6x A78 + 1024 CUDA)", 5.0, 3.0, 15.0, 40, "GbE / USB3 / PCIe",
     "NVIDIA", "Jetson Orin Nano", "edge-AI robotics SBC"),
    ("beaglebone_black", "sbc", (86, 53, 15), 0.040, PCB_GREEN,
     "AM3358 (Cortex-A8)", 5.0, 0.5, 2.5, 65, "Ethernet / USB", "BeagleBoard",
     "BeagleBone Black", "SBC with PRU real-time cores"),
    ("radxa_zero", "sbc", (65, 30, 8), 0.015, PCB_GREEN,
     "S905Y2 (quad A53)", 5.0, 0.8, 4.0, 40, "WiFi / USB-C", "Radxa",
     "Zero", "Pi-Zero-format Amlogic SBC"),
    ("libre_lepotato", "sbc", (85, 56, 19), 0.045, PCB_GREEN,
     "S905X (quad A53)", 5.0, 1.0, 5.0, 40, "GbE / USB", "Libre Computer",
     "AML-S905X-CC", "Raspberry-Pi-compatible SBC"),
]


def _make(row):
    (slug, category, dims, mass, color, chip, logic_v, current, power_w,
     gpio, connectivity, mfr, pn, notes) = row

    def factory():
        part = ControllerBoard(slug)
        part.build_box(
            dims[0], dims[1], dims[2], mass_kg=mass, color=color,
            power=PowerSpec(nominal_voltage_v=logic_v, current_a=current,
                            power_w=power_w),
            manufacturer=mfr, part_number=pn, notes=notes,
        )
        part.category = category
        part.chip = chip
        part.logic_voltage = logic_v
        part.gpio = gpio
        part.connectivity = connectivity
        return part

    factory.__doc__ = (
        f"{notes}. {chip}, {logic_v} V logic, {gpio} GPIO, {connectivity}. "
        f"{mfr} {pn}."
    )
    return register(slug, category, factory, manufacturer=mfr, part_number=pn,
                    summary=notes)


for _row in _ITEMS:
    globals()[f"get_{_row[0]}"] = _make(_row)

__all__ = ["ControllerBoard"] + [f"get_{r[0]}" for r in _ITEMS]
