from utilities import Dimension, getDimensionsFromString, LengthUnit, convertToLengthUnit, getAnglesFromString, AngleUnit, Angle

def test_dimensions():
    dimension = Dimension("")
    assert dimension.value == None
    assert dimension.unit == None
    dimension = Dimension("50")
    assert dimension.value == 50
    assert dimension.unit == None
    dimension = Dimension("100")
    assert dimension.value == 100
    assert dimension.unit == None
    dimension = Dimension("100", LengthUnit.meter)
    assert dimension.value == 100
    assert dimension.unit == LengthUnit.meter
    dimension = Dimension(99, LengthUnit.meter)
    assert dimension.value == 99
    assert dimension.unit == LengthUnit.meter

    dimension = Dimension("100mm")
    assert dimension.value == 100
    assert dimension.unit == LengthUnit.millimeter
    dimension = Dimension("1m")
    assert dimension.value == 1
    assert dimension.unit == LengthUnit.meter
    
    dimension = Dimension("1/4mm")
    assert dimension.value == 0.25
    assert dimension.unit == LengthUnit.millimeter
    dimension = Dimension("1-(3/4)")
    assert dimension.value == 0.25
    assert dimension.unit == None
    dimension = Dimension("1-(3/4)", LengthUnit.foot)
    assert dimension.value == 0.25
    assert dimension.unit == LengthUnit.foot

    dimensions = getDimensionsFromString(",1cm,")
    assert dimensions[0].value == None and dimensions[1].value == 1
    assert dimensions[0].unit == None and dimensions[1].unit == LengthUnit.centimeter
    dimensions = getDimensionsFromString("10,1")
    assert dimensions[0].value == 10 and dimensions[1].value == 1
    assert dimensions[0].unit == None and dimensions[1].unit == None
    dimensions = getDimensionsFromString("1,2,m")
    assert dimensions[0].value == 1 and dimensions[1].value == 2
    assert dimensions[0].unit == LengthUnit.meter and dimensions[1].unit == LengthUnit.meter
    dimensions = getDimensionsFromString("1,2,3,m")
    assert dimensions[0].value == 1 and dimensions[1].value == 2 and dimensions[2].value == 3
    assert dimensions[0].unit == LengthUnit.meter and dimensions[1].unit == LengthUnit.meter and dimensions[2].unit == LengthUnit.meter
    dimensions = getDimensionsFromString("1m,2m,3m")
    assert dimensions[0].value == 1 and dimensions[1].value == 2 and dimensions[2].value == 3
    assert dimensions[0].unit == LengthUnit.meter and dimensions[1].unit == LengthUnit.meter and dimensions[2].unit == LengthUnit.meter
    dimensions = getDimensionsFromString("1,2,3mm,m")
    assert dimensions[0].value == 1 and dimensions[1].value == 2 and dimensions[2].value == 3
    assert dimensions[0].unit == LengthUnit.meter and dimensions[1].unit == LengthUnit.meter and dimensions[2].unit == LengthUnit.millimeter
    dimensions = getDimensionsFromString("21,1/8,1/8, in")
    assert dimensions[0].value == 21 and dimensions[1].value == .125 and dimensions[2].value == .125
    assert dimensions[0].unit == LengthUnit.inch and dimensions[1].unit == LengthUnit.inch and dimensions[2].unit == LengthUnit.inch

    assert convertToLengthUnit(LengthUnit.millimeter, 1, LengthUnit.meter) == 1000
    assert convertToLengthUnit(LengthUnit.meter, 1000, LengthUnit.millimeter) == 1

    print("test_dimensions done.")

def test_angles():
    angles = getAnglesFromString("10,1")
    assert angles[0].value == 10 and angles[1].value == 1
    assert angles[0].unit == AngleUnit.RADIANS and angles[1].unit == AngleUnit.RADIANS
    angles = getAnglesFromString("1,2,deg")
    assert angles[0].value == 1 and angles[1].value == 2
    assert angles[0].unit == AngleUnit.DEGREES and angles[1].unit == AngleUnit.DEGREES
    angles = getAnglesFromString("1,2,3,deg")
    assert angles[0].value == 1 and angles[1].value == 2 and angles[2].value == 3
    assert angles[0].unit == AngleUnit.DEGREES and angles[1].unit == AngleUnit.DEGREES and angles[2].unit == AngleUnit.DEGREES
    angles = getAnglesFromString("1deg,2rad,3deg")
    assert angles[0].value == 1 and angles[1].value == 2 and angles[2].value == 3
    assert angles[0].unit == AngleUnit.DEGREES and angles[1].unit == AngleUnit.RADIANS and angles[2].unit == AngleUnit.DEGREES
    angles = getAnglesFromString("1,2,3deg,rad")
    assert angles[0].value == 1 and angles[1].value == 2 and angles[2].value == 3
    assert angles[0].unit == AngleUnit.RADIANS and angles[1].unit == AngleUnit.RADIANS and angles[2].unit == AngleUnit.DEGREES
    angles = getAnglesFromString("21,1/8,1/8, degrees")
    assert angles[0].value == 21 and angles[1].value == .125 and angles[2].value == .125
    assert angles[0].unit == AngleUnit.DEGREES and angles[1].unit == AngleUnit.DEGREES and angles[2].unit == AngleUnit.DEGREES

    print("test_angles done")


    
test_dimensions()

test_angles()