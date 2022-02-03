from blender.utilities import Length, convertToMillimeters, convertToUnit
from utilities import Dimension, Units, getDimensionsFromString

def test_dimensions():
    dimension = Dimension("50")
    assert dimension.value == 50
    assert dimension.unit == None
    dimension = Dimension("100")
    assert dimension.value == 100
    assert dimension.unit == None
    dimension = Dimension("100", Length.meter)
    assert dimension.value == 100
    assert dimension.unit == Length.meter
    dimension = Dimension(99, Length.meter)
    assert dimension.value == 99
    assert dimension.unit == Length.meter

    dimension = Dimension("100mm")
    assert dimension.value == 100
    assert dimension.unit == Length.millimeter
    dimension = Dimension("1m")
    assert dimension.value == 1
    assert dimension.unit == Length.meter
    
    dimension = Dimension("1/4mm")
    assert dimension.value == 0.25
    assert dimension.unit == Length.millimeter
    dimension = Dimension("1-(3/4)")
    assert dimension.value == 0.25
    assert dimension.unit == None
    dimension = Dimension("1-(3/4)", Length.foot)
    assert dimension.value == 0.25
    assert dimension.unit == Length.foot


    dimensions = getDimensionsFromString("10,1")
    assert dimensions[0].value == 10 and dimensions[1].value == 1
    assert dimensions[0].unit == None and dimensions[1].unit == None
    dimensions = getDimensionsFromString("1,2,m")
    assert dimensions[0].value == 1 and dimensions[1].value == 2
    assert dimensions[0].unit == Length.meter and dimensions[1].unit == Length.meter
    dimensions = getDimensionsFromString("1,2,3,m")
    assert dimensions[0].value == 1 and dimensions[1].value == 2 and dimensions[2].value == 3
    assert dimensions[0].unit == Length.meter and dimensions[1].unit == Length.meter and dimensions[2].unit == Length.meter
    dimensions = getDimensionsFromString("1m,2m,3m")
    assert dimensions[0].value == 1 and dimensions[1].value == 2 and dimensions[2].value == 3
    assert dimensions[0].unit == Length.meter and dimensions[1].unit == Length.meter and dimensions[2].unit == Length.meter
    dimensions = getDimensionsFromString("1,2,3mm,m")
    assert dimensions[0].value == 1 and dimensions[1].value == 2 and dimensions[2].value == 3
    assert dimensions[0].unit == Length.meter and dimensions[1].unit == Length.meter and dimensions[2].unit == Length.millimeter
    dimensions = getDimensionsFromString("21,1/8,1/8, in")
    assert dimensions[0].value == 21 and dimensions[1].value == .125 and dimensions[2].value == .125
    assert dimensions[0].unit == Length.inch and dimensions[1].unit == Length.inch and dimensions[2].unit == Length.inch

    
    assert convertToMillimeters(1, Length.meter) == 1000
    assert convertToMillimeters(21, Length.inch) == 533.4
    assert convertToMillimeters(1/8, Length.inch) == 3.175

    assert convertToUnit(Length.millimeter, 1, Length.meter) == 1000
    assert convertToUnit(Length.meter, 1000, Length.millimeter) == 1

    print("test_dimensions done.")

test_dimensions()