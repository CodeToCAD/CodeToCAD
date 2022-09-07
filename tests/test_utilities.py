from utilities import Dimension, LengthUnit, AngleUnit, Angle,getAnglesFromStringList, getDimensionsFromStringList,BoundaryAxis, BoundaryBox

def test_dimensions():
    try:
        dimension = Dimension.fromString("")
        assert False
    except Exception as e:
        assert str(e) == "Dimension value cannot be empty."
    dimension = Dimension.fromString("50")
    assert dimension.value == 50
    assert dimension.unit == None
    dimension = Dimension.fromString("100")
    assert dimension.value == 100
    assert dimension.unit == None
    dimension = Dimension.fromString("100", LengthUnit.meter)
    assert dimension.value == 100
    assert dimension.unit == LengthUnit.meter
    dimension = Dimension(99, LengthUnit.meter)
    assert dimension.value == 99
    assert dimension.unit == LengthUnit.meter

    dimension = Dimension.fromString("100mm")
    assert dimension.value == 100
    assert dimension.unit == LengthUnit.millimeter
    dimension = Dimension.fromString("1m")
    assert dimension.value == 1
    assert dimension.unit == LengthUnit.meter
    
    dimension = Dimension.fromString("1/4mm")
    assert dimension.value == 0.25
    assert dimension.unit == LengthUnit.millimeter
    dimension = Dimension.fromString("1-(3/4)")
    assert dimension.value == 0.25
    assert dimension.unit == None
    dimension = Dimension.fromString("1-(3/4)", LengthUnit.foot)
    assert dimension.value == 0.25
    assert dimension.unit == LengthUnit.foot

    dimensions = getDimensionsFromStringList("10,1")
    assert dimensions[0].value == 10 and dimensions[1].value == 1
    assert dimensions[0].unit == None and dimensions[1].unit == None
    dimensions = getDimensionsFromStringList("1,2,m")
    assert dimensions[0].value == 1 and dimensions[1].value == 2
    assert dimensions[0].unit == LengthUnit.meter and dimensions[1].unit == LengthUnit.meter
    dimensions = getDimensionsFromStringList("1,2,3,m")
    assert dimensions[0].value == 1 and dimensions[1].value == 2 and dimensions[2].value == 3
    assert dimensions[0].unit == LengthUnit.meter and dimensions[1].unit == LengthUnit.meter and dimensions[2].unit == LengthUnit.meter
    dimensions = getDimensionsFromStringList("1m,2m,3m")
    assert dimensions[0].value == 1 and dimensions[1].value == 2 and dimensions[2].value == 3
    assert dimensions[0].unit == LengthUnit.meter and dimensions[1].unit == LengthUnit.meter and dimensions[2].unit == LengthUnit.meter
    dimensions = getDimensionsFromStringList("1m,2in,3m")
    assert dimensions[0].value == 1 and dimensions[1].value == 2 and dimensions[2].value == 3
    assert dimensions[0].unit == LengthUnit.meter and dimensions[1].unit == LengthUnit.inch and dimensions[2].unit == LengthUnit.meter
    dimensions = getDimensionsFromStringList("1,2,3mm,m")
    assert dimensions[0].value == 1 and dimensions[1].value == 2 and dimensions[2].value == 3
    assert dimensions[0].unit == LengthUnit.meter and dimensions[1].unit == LengthUnit.meter and dimensions[2].unit == LengthUnit.millimeter
    dimensions = getDimensionsFromStringList("21,1/8,1/8, in")
    assert dimensions[0].value == 21 and dimensions[1].value == .125 and dimensions[2].value == .125
    assert dimensions[0].unit == LengthUnit.inch and dimensions[1].unit == LengthUnit.inch and dimensions[2].unit == LengthUnit.inch

    assert Dimension(1, LengthUnit.meter).convertToUnit(LengthUnit.millimeter).value == 1000
    assert Dimension(1000, LengthUnit.millimeter).convertToUnit(LengthUnit.meter).value == 1

    print("test_dimensions done.")

def test_minMaxCenter():
    
    boundingBox = BoundaryBox(
        BoundaryAxis(
            -1, 1, 0, LengthUnit.meter
        ),
        BoundaryAxis(
            -1, 1, 0, LengthUnit.meter
        ),
        BoundaryAxis(
            -1, 1, 0, LengthUnit.meter
        )
    )

    dimensions = getDimensionsFromStringList("min", boundingBox)
    assert dimensions[0].value == -1
    assert dimensions[0].unit == LengthUnit.meter
    dimensions = getDimensionsFromStringList("max", boundingBox)
    assert dimensions[0].value == 1
    assert dimensions[0].unit == LengthUnit.meter
    dimensions = getDimensionsFromStringList("center", boundingBox)
    assert dimensions[0].value == 0
    assert dimensions[0].unit == LengthUnit.meter
    dimensions = getDimensionsFromStringList("min-2", boundingBox)
    assert dimensions[0].value == -3
    assert dimensions[0].unit == LengthUnit.meter
    dimensions = getDimensionsFromStringList("min-2cm", boundingBox)
    assert dimensions[0].value == -102
    assert dimensions[0].unit == LengthUnit.centimeter

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