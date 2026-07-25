"""Human-machine interface & signalling parts: displays, LEDs, buzzers,
relays, potentiometers and indicators -- the I/O a robot uses to talk to
people. Each returns a ``Part3D`` at the real module size with electrical
ratings and part-specific attributes (``resolution``, ``channels`` ...).
"""

from __future__ import annotations

from ._base import (
    BODY_BLACK,
    BODY_RED,
    PCB_GREEN,
    PassivePart,
    PowerSpec,
    register,
)


class HMIComponent(PassivePart):
    category = "hmi"


# slug, category, (l,w,h), mass, color, voltage, current_A, extra{}, mfr, pn, notes
_ITEMS = [
    # --- displays ---
    ("oled_ssd1306_096", "display", (27, 27, 4), 0.006, PCB_GREEN, 3.3, 0.02,
     {"resolution": (128, 64), "interface": "I2C"}, "Generic", "SSD1306 0.96\"",
     "128x64 monochrome OLED"),
    ("oled_sh1106_13", "display", (36, 33, 4), 0.009, PCB_GREEN, 3.3, 0.03,
     {"resolution": (128, 64), "interface": "I2C"}, "Generic", "SH1106 1.3\"",
     "1.3 inch monochrome OLED"),
    ("lcd_1602_i2c", "display", (80, 36, 19), 0.045, PCB_GREEN, 5.0, 0.03,
     {"resolution": (16, 2), "interface": "I2C"}, "Generic", "1602 + PCF8574",
     "16x2 character LCD with I2C backpack"),
    ("tft_ili9341_24", "display", (72, 52, 4), 0.030, PCB_GREEN, 3.3, 0.10,
     {"resolution": (320, 240), "interface": "SPI"}, "Generic", "ILI9341 2.4\"",
     "320x240 color TFT (touch)"),
    ("eink_29", "display", (37, 89, 4), 0.020, BODY_BLACK, 3.3, 0.02,
     {"resolution": (296, 128), "interface": "SPI"}, "WaveShare", "2.9\" e-Paper",
     "2.9 inch e-ink display"),
    # --- indicators ---
    ("led_5mm", "indicator", (5, 5, 9), 0.0003, BODY_RED, 2.0, 0.02,
     {"color": "red", "forward_v": 2.0}, "Generic", "5mm LED", "5 mm through-hole LED"),
    ("led_3mm", "indicator", (3, 3, 6), 0.0002, BODY_RED, 2.0, 0.02,
     {"color": "red", "forward_v": 2.0}, "Generic", "3mm LED", "3 mm through-hole LED"),
    ("ws2812b_pixel", "indicator", (5, 5, 1.6), 0.0002, BODY_BLACK, 5.0, 0.06,
     {"channels": 1, "interface": "1-wire"}, "WorldSemi", "WS2812B",
     "addressable RGB LED (NeoPixel)"),
    ("neopixel_ring_16", "indicator", (44, 44, 3), 0.008, BODY_BLACK, 5.0, 0.96,
     {"channels": 16, "interface": "1-wire"}, "Adafruit", "NeoPixel Ring 16",
     "16-LED addressable RGB ring"),
    ("led_bar_10", "indicator", (25, 10, 8), 0.003, BODY_RED, 2.0, 0.20,
     {"channels": 10}, "Generic", "10-seg bargraph", "10-segment LED bar"),
    # --- audio ---
    ("buzzer_active", "audio", (12, 12, 9), 0.002, BODY_BLACK, 5.0, 0.03,
     {"type": "active"}, "Generic", "active buzzer", "active piezo buzzer (fixed tone)"),
    ("buzzer_passive", "audio", (12, 12, 9), 0.002, BODY_BLACK, 5.0, 0.03,
     {"type": "passive"}, "Generic", "passive buzzer", "passive piezo (PWM tones)"),
    ("speaker_8ohm_1w", "audio", (40, 40, 5), 0.010, BODY_BLACK, 5.0, 0.2,
     {"impedance_ohm": 8, "power_w": 1}, "Generic", "8ohm 1W", "small 8 ohm speaker"),
    # --- controls / switching ---
    ("potentiometer_10k", "control", (16, 16, 25), 0.010, BODY_BLACK, 5.0, 0.001,
     {"resistance_ohm": 10000, "taper": "linear"}, "Generic", "B10K pot",
     "10k rotary potentiometer with shaft"),
    ("relay_module_1ch", "control", (50, 26, 19), 0.020, PCB_GREEN, 5.0, 0.07,
     {"channels": 1, "contact": "10A 250VAC"}, "Generic", "1-ch relay",
     "opto-isolated relay module"),
    ("relay_module_4ch", "control", (75, 55, 19), 0.055, PCB_GREEN, 5.0, 0.28,
     {"channels": 4, "contact": "10A 250VAC"}, "Generic", "4-ch relay",
     "4-channel relay module"),
    ("mosfet_module_irf520", "control", (34, 25, 18), 0.012, PCB_GREEN, 24, 5,
     {"switch": "low-side N-MOSFET"}, "Generic", "IRF520 module",
     "logic-level MOSFET switch module"),
]


def _make(row):
    (slug, category, dims, mass, color, voltage, current, extra, mfr, pn,
     notes) = row

    def factory():
        part = HMIComponent(slug)
        part.build_box(
            dims[0], dims[1], dims[2], mass_kg=mass, color=color,
            power=PowerSpec(nominal_voltage_v=voltage, current_a=current),
            manufacturer=mfr, part_number=pn, notes=notes,
        )
        part.category = category
        for key, value in extra.items():
            setattr(part, key, value)
        return part

    factory.__doc__ = f"{notes}. {voltage} V. {mfr} {pn}."
    return register(slug, category, factory, manufacturer=mfr, part_number=pn,
                    summary=notes)


for _row in _ITEMS:
    globals()[f"get_{_row[0]}"] = _make(_row)

__all__ = ["HMIComponent"] + [f"get_{r[0]}" for r in _ITEMS]
