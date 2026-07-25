"""Power: batteries, DC-DC converters / regulators, bench supplies and
protection. Each returns a ``Part3D`` sized to the real module with its
electrical ratings on ``part.power`` plus part-specific attributes
(``capacity_mah``, ``output_v``, ``chemistry`` ...).
"""

from __future__ import annotations

from ._base import (
    BODY_BLACK,
    BODY_BLUE,
    BODY_STEEL,
    PCB_GREEN,
    PassivePart,
    PowerSpec,
    register,
)


class PowerComponent(PassivePart):
    category = "power"


# (slug, category, shape, dims(l,w,h|dia,h), mass_kg, color, voltage, current,
#  power_w, extra{}, mfr, pn, notes)
_ITEMS = [
    # --- batteries ---
    ("lipo_1s_450", "battery", "box", (35, 20, 6), 0.011, BODY_BLUE, 3.7, 9, None,
     {"capacity_mah": 450, "chemistry": "LiPo", "cells": 1},
     "Generic", "1S 450mAh", "1S LiPo (micro drones)"),
    ("lipo_2s_1000", "battery", "box", (72, 35, 12), 0.060, BODY_BLUE, 7.4, 25, None,
     {"capacity_mah": 1000, "chemistry": "LiPo", "cells": 2},
     "Generic", "2S 1000mAh", "2S LiPo pack"),
    ("lipo_3s_2200", "battery", "box", (105, 34, 24), 0.185, BODY_BLUE, 11.1, 55, None,
     {"capacity_mah": 2200, "chemistry": "LiPo", "cells": 3},
     "Generic", "3S 2200mAh", "3S LiPo (FPV / small robots)"),
    ("lipo_4s_5000", "battery", "box", (145, 50, 25), 0.480, BODY_BLUE, 14.8, 250, None,
     {"capacity_mah": 5000, "chemistry": "LiPo", "cells": 4},
     "Generic", "4S 5000mAh", "4S LiPo (large multirotors / rovers)"),
    ("li18650_cell", "battery", "cyl", (18.4, 65), 0.048, BODY_STEEL, 3.7, 10, None,
     {"capacity_mah": 3500, "chemistry": "Li-ion", "cells": 1},
     "Generic", "18650", "Li-ion 18650 cell"),
    ("li21700_cell", "battery", "cyl", (21, 70), 0.070, BODY_STEEL, 3.7, 15, None,
     {"capacity_mah": 5000, "chemistry": "Li-ion", "cells": 1},
     "Generic", "21700", "Li-ion 21700 cell (higher capacity)"),
    ("lifepo4_12v_6ah", "battery", "box", (151, 65, 95), 0.900, BODY_STEEL, 12.8, 18, None,
     {"capacity_mah": 6000, "chemistry": "LiFePO4", "cells": 4},
     "Generic", "12V 6Ah", "12.8 V LiFePO4 pack"),
    ("aa_holder_4", "battery", "box", (58, 58, 15), 0.030, BODY_BLACK, 6.0, 2, None,
     {"capacity_mah": 2000, "chemistry": "alkaline", "cells": 4},
     "Generic", "4xAA holder", "4-cell AA battery holder"),
    ("battery_9v", "battery", "box", (48, 26, 17), 0.045, BODY_BLACK, 9.0, 0.5, None,
     {"capacity_mah": 550, "chemistry": "alkaline", "cells": 1},
     "Generic", "9V (PP3)", "9 V block battery"),
    ("coin_cr2032", "battery", "cyl", (20, 3.2), 0.003, BODY_STEEL, 3.0, 0.02, None,
     {"capacity_mah": 220, "chemistry": "Li coin", "cells": 1},
     "Generic", "CR2032", "3 V coin cell (RTC / small logic)"),
    # --- DC-DC converters / regulators ---
    ("buck_lm2596", "converter", "box", (43, 21, 14), 0.011, PCB_GREEN, 40, 3, 15,
     {"input_range": "3-40 V", "output_v": "1.5-35 V", "topology": "buck"},
     "TI", "LM2596", "adjustable step-down module"),
    ("buck_mp1584", "converter", "box", (22, 17, 4), 0.002, PCB_GREEN, 28, 3, 15,
     {"input_range": "4.5-28 V", "output_v": "0.8-20 V", "topology": "buck"},
     "MPS", "MP1584EN", "mini step-down module"),
    ("boost_xl6009", "converter", "box", (43, 21, 14), 0.011, PCB_GREEN, 32, 3, 15,
     {"input_range": "3-32 V", "output_v": "5-35 V", "topology": "boost"},
     "XLSEMI", "XL6009", "adjustable step-up module"),
    ("buckboost_sepic", "converter", "box", (48, 23, 15), 0.013, PCB_GREEN, 32, 2, 15,
     {"input_range": "3-30 V", "output_v": "1.2-35 V", "topology": "buck-boost"},
     "Generic", "SEPIC", "buck-boost converter module"),
    ("ubec_5v_3a", "converter", "box", (30, 12, 8), 0.008, BODY_BLACK, 26, 3, 15,
     {"input_range": "6-26 V", "output_v": "5 V", "topology": "buck BEC"},
     "Generic", "5V 3A UBEC", "switching BEC for RC electronics"),
    ("pololu_d24v22f5", "converter", "box", (17.8, 10.2, 4, ), 0.002, PCB_GREEN, 36, 2.4, 12,
     {"input_range": "6-36 V", "output_v": "5 V", "topology": "buck"},
     "Pololu", "D24V22F5", "compact 5 V step-down"),
    ("vreg_7805", "regulator", "box", (10.2, 4.6, 15), 0.003, BODY_BLACK, 35, 1, 5,
     {"input_range": "7-35 V", "output_v": "5 V", "topology": "linear"},
     "ST", "L7805", "5 V linear regulator (TO-220)"),
    ("vreg_ams1117_33", "regulator", "box", (6.5, 3.5, 2.3), 0.001, BODY_BLACK, 15, 1, 3,
     {"input_range": "4.5-15 V", "output_v": "3.3 V", "topology": "linear LDO"},
     "AMS", "AMS1117-3.3", "3.3 V LDO regulator"),
    # --- bench / brick supplies ---
    ("psu_5v_10a", "supply", "box", (110, 80, 37), 0.400, BODY_STEEL, 5, 10, 50,
     {"input_range": "100-240 VAC", "output_v": "5 V"},
     "Generic", "5V 10A", "enclosed 5 V switching PSU"),
    ("psu_12v_10a", "supply", "box", (200, 98, 42), 0.700, BODY_STEEL, 12, 10, 120,
     {"input_range": "100-240 VAC", "output_v": "12 V"},
     "Generic", "12V 10A", "12 V switching PSU (LED / CNC)"),
    ("psu_meanwell_lrs350_24", "supply", "box", (215, 115, 30), 0.850, BODY_STEEL, 24, 14.6, 350,
     {"input_range": "85-264 VAC", "output_v": "24 V"},
     "MeanWell", "LRS-350-24", "24 V 350 W enclosed PSU (3D printers)"),
    # --- protection ---
    ("blade_fuse_holder", "protection", "box", (60, 20, 20), 0.010, BODY_BLACK, 32, 30, None,
     {"fuse": "ATC/ATO blade"}, "Generic", "ATC holder", "inline blade-fuse holder"),
    ("ptc_resettable_1a", "protection", "box", (7, 3, 8), 0.001, BODY_STEEL, 30, 1, None,
     {"hold_current_a": 1.0}, "Bourns", "MF-R", "resettable PTC fuse"),
    ("rocker_switch_spst", "protection", "box", (21, 15, 23), 0.008, BODY_BLACK, 250, 6, None,
     {"poles": "SPST"}, "Generic", "KCD1", "panel rocker power switch"),
]


def _make(row):
    (slug, category, shape, dims, mass, color, voltage, current, power_w,
     extra, mfr, pn, notes) = row

    def factory():
        part = PowerComponent(slug)
        p = PowerSpec(nominal_voltage_v=voltage, current_a=current,
                      power_w=power_w)
        if shape == "cyl":
            part.build_cylinder(dims[0], dims[1], mass_kg=mass, color=color,
                                power=p, manufacturer=mfr, part_number=pn,
                                notes=notes)
        else:
            part.build_box(dims[0], dims[1], dims[2], mass_kg=mass, color=color,
                           power=p, manufacturer=mfr, part_number=pn, notes=notes)
        part.category = category
        for key, value in extra.items():
            setattr(part, key, value)
        return part

    factory.__doc__ = f"{notes}. {voltage} V. {mfr} {pn}."
    return register(slug, category, factory, manufacturer=mfr, part_number=pn,
                    summary=notes)


for _row in _ITEMS:
    globals()[f"get_{_row[0]}"] = _make(_row)

__all__ = ["PowerComponent"] + [f"get_{r[0]}" for r in _ITEMS]
