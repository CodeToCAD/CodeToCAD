import math
import pytest

from codetocad.cad import *


def test_length():
    x = Length("2mm + 1m")
    assert math.isclose(x, 1.002), f"Expected 1.002m but got {x}m"

    x = Length("5in")
    assert math.isclose(x, 0.127), f"Expected 0.127m but got {x}m"

    x = Length(f"2mm * {x}")
    assert math.isclose(x, 0.000254), f"Expected 0.000254m but got {x}m"


def test_angle():
    theta = Angle("90deg + 0.5rad")
    assert math.isclose(
        theta, 2.0708, abs_tol=0.0001
    ), f"Expected 2.0708rad but got {theta}rad"


def test_sketch():
    sketch = Sketch()

    t = Length("5mm")
    gap = Length("2mm")
    sketch.draw.point("0mm", "0mm")
    sketch.draw.line_to(f"10cm + 2*{t} + {gap}", "0")
    sketch.draw.line_to("20cm", "10cm")

    wire = sketch.get.wire(-1)
    e1 = wire.get.edge(0)
    e2 = wire.get.edge(1)

    wire.constraint.parallel(e1, e2)

    v_mid = sketch.draw.point("0", "0").v1
    wire.constraint.midpoint(e1, v_mid)

    print(sketch)
    for e in sketch.wires:
        print(e)


def test_assembly():
    my_assembly = Assembly()
    p0 = my_assembly.add.preset.cube("1", "0.2", "0.2")
    p1 = my_assembly.add.preset.cube(1, 1, 1)
    p2 = my_assembly.add.preset.cube(2, 2, 2)

    p1.set_name("my_beam")
    found = Part.get_by_name("my_beam")

    print(my_assembly.get.parts)
    print(my_assembly.get.part("my_beam").name)
    print(my_assembly.get.part["my_beam"].name)
    print(my_assembly.get.part[1].name)
    print(my_assembly.get.part[-2].name)
