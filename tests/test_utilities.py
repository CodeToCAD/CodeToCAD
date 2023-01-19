from core.utilities import Dimension, LengthUnit, AngleUnit, Angle, getAnglesFromStringList, getDimensionListFromStringList, BoundaryAxis, BoundaryBox


def test_dimensions():
    try:
        dimension = Dimension.fromString("")
        assert False
    except Exception as e:
        assert str(e) == "Dimension value cannot be empty."

    try:
        dimension = Dimension.fromString("50NotAUnit")
        assert False
    except Exception as e:
        assert "Could not parse unit" in str(e)

    dimension = Dimension.fromString("50")
    assert dimension.value == 50
    assert dimension.unit == None
    dimension = Dimension.fromString("100")
    assert dimension.value == 100
    assert dimension.unit == None
    dimension = Dimension.fromString("100", LengthUnit.m)
    assert dimension.value == 100
    assert dimension.unit == LengthUnit.m
    dimension = Dimension(99, LengthUnit.m)
    assert dimension.value == 99
    assert dimension.unit == LengthUnit.m

    dimension = Dimension.fromString("100mm")
    assert dimension.value == 100
    assert dimension.unit == LengthUnit.mm
    dimension = Dimension.fromString("1m")
    assert dimension.value == 1
    assert dimension.unit == LengthUnit.m

    dimension = Dimension.fromString("1/4mm")
    assert dimension.value == 0.25
    assert dimension.unit == LengthUnit.mm
    dimension = Dimension.fromString("1-(3/4)")
    assert dimension.value == 0.25
    assert dimension.unit == None
    dimension = Dimension.fromString("1-(3/4)", LengthUnit.ft)
    assert dimension.value == 0.25
    assert dimension.unit == LengthUnit.ft

    dimensions = getDimensionListFromStringList("10,1")
    assert dimensions[0].value == 10 and dimensions[1].value == 1
    assert dimensions[0].unit == None and dimensions[1].unit == None
    dimensions = getDimensionListFromStringList("1,2,m")
    assert dimensions[0].value == 1 and dimensions[1].value == 2
    assert dimensions[0].unit == LengthUnit.m and dimensions[1].unit == LengthUnit.m
    dimensions = getDimensionListFromStringList("1,2,3,m")
    assert dimensions[0].value == 1 and dimensions[1].value == 2 and dimensions[2].value == 3
    assert dimensions[0].unit == LengthUnit.m and dimensions[1].unit == LengthUnit.m and dimensions[2].unit == LengthUnit.m
    dimensions = getDimensionListFromStringList("1m,2m,3m")
    assert dimensions[0].value == 1 and dimensions[1].value == 2 and dimensions[2].value == 3
    assert dimensions[0].unit == LengthUnit.m and dimensions[1].unit == LengthUnit.m and dimensions[2].unit == LengthUnit.m
    dimensions = getDimensionListFromStringList("1m,2in,3m")
    assert dimensions[0].value == 1 and dimensions[1].value == 2 and dimensions[2].value == 3
    assert dimensions[0].unit == LengthUnit.m and dimensions[1].unit == LengthUnit.inch and dimensions[2].unit == LengthUnit.m
    dimensions = getDimensionListFromStringList("1,2,3mm,m")
    assert dimensions[0].value == 1 and dimensions[1].value == 2 and dimensions[2].value == 3
    assert dimensions[0].unit == LengthUnit.m and dimensions[1].unit == LengthUnit.m and dimensions[2].unit == LengthUnit.mm
    dimensions = getDimensionListFromStringList("21,1/8,1/8, in")
    assert dimensions[0].value == 21 and dimensions[1].value == .125 and dimensions[2].value == .125
    assert dimensions[0].unit == LengthUnit.inch and dimensions[1].unit == LengthUnit.inch and dimensions[2].unit == LengthUnit.inch
    dimensions = getDimensionListFromStringList("3in,1mm")
    assert dimensions[0].value == 3 and dimensions[1].value == 1
    assert dimensions[0].unit == LengthUnit.inch and dimensions[1].unit == LengthUnit.mm

    assert Dimension(1, LengthUnit.m).convertToUnit(
        LengthUnit.mm).value == 1000
    assert Dimension(1000, LengthUnit.mm).convertToUnit(
        LengthUnit.m).value == 1

    print("test_dimensions done.")


def test_minMaxCenter():

    boundingBox = BoundaryBox(
        BoundaryAxis(
            -1, 1, LengthUnit.m
        ),
        BoundaryAxis(
            -1, 1, LengthUnit.m
        ),
        BoundaryAxis(
            -1, 1, LengthUnit.m
        )
    )

    dimensions = getDimensionListFromStringList("min", boundingBox)
    assert dimensions[0].value == -1
    assert dimensions[0].unit == LengthUnit.m
    dimensions = getDimensionListFromStringList("max", boundingBox)
    assert dimensions[0].value == 1
    assert dimensions[0].unit == LengthUnit.m
    dimensions = getDimensionListFromStringList("center", boundingBox)
    assert dimensions[0].value == 0
    assert dimensions[0].unit == LengthUnit.m
    dimensions = getDimensionListFromStringList("min-2", boundingBox)
    assert dimensions[0].value == -3
    assert dimensions[0].unit == LengthUnit.m
    dimensions = getDimensionListFromStringList("min-2cm", boundingBox)
    assert dimensions[0].value == -102
    assert dimensions[0].unit == LengthUnit.cm

    print("test_minMaxCenter() done.")


def test_angles():
    angles = getAnglesFromStringList("10,1")
    assert angles[0].value == 10 and angles[1].value == 1
    assert angles[0].unit == AngleUnit.DEGREES and angles[1].unit == AngleUnit.DEGREES
    angles = getAnglesFromStringList("1,2,deg")
    assert angles[0].value == 1 and angles[1].value == 2
    assert angles[0].unit == AngleUnit.DEGREES and angles[1].unit == AngleUnit.DEGREES
    angles = getAnglesFromStringList("1,2,3,deg")
    assert angles[0].value == 1 and angles[1].value == 2 and angles[2].value == 3
    assert angles[0].unit == AngleUnit.DEGREES and angles[1].unit == AngleUnit.DEGREES and angles[2].unit == AngleUnit.DEGREES
    angles = getAnglesFromStringList("1deg,2rad,3deg")
    assert angles[0].value == 1 and angles[1].value == 2 and angles[2].value == 3
    assert angles[0].unit == AngleUnit.DEGREES and angles[1].unit == AngleUnit.RADIANS and angles[2].unit == AngleUnit.DEGREES
    angles = getAnglesFromStringList("1,2,3deg,rad")
    assert angles[0].value == 1 and angles[1].value == 2 and angles[2].value == 3
    assert angles[0].unit == AngleUnit.RADIANS and angles[1].unit == AngleUnit.RADIANS and angles[2].unit == AngleUnit.DEGREES
    angles = getAnglesFromStringList("21,1/8,1/8, degrees")
    assert angles[0].value == 21 and angles[1].value == .125 and angles[2].value == .125
    assert angles[0].unit == AngleUnit.DEGREES and angles[1].unit == AngleUnit.DEGREES and angles[2].unit == AngleUnit.DEGREES

    print("test_angles done")


if __name__ == "__main__":
    test_dimensions()
    test_minMaxCenter()
    test_angles()
