from utilities import Dimension, Units, getDimensionsFromString

def test_dimensions():
    assert Dimension("100").value == 100
    assert Dimension("100mm").value == 100
    assert Dimension("1m").value == 1000
    assert Dimension("1", Units.meter).value == 1000
    assert Dimension("1/4mm").value == 0.25
    assert Dimension("1-(3/4)").value == 0.25 
    assert getDimensionsFromString("10,1") == [10,1]
    assert getDimensionsFromString("1,1,m") == [1000,1000]
    assert getDimensionsFromString("1,1,1,m") == [1000,1000,1000]
    assert getDimensionsFromString("1m,1m,1m") == [1000,1000,1000]
    assert getDimensionsFromString("1,1,1mm,m") == [1000,1000,1]
    assert getDimensionsFromString("21,1/8,1/8, in") == [533.4,3.175,3.175]
    print("test_dimensions done.")

test_dimensions()