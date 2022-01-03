from utilities import Dimension

def test_dimensions():
    assert Dimension("100").value == 100
    assert Dimension("100mm").value == 100
    assert Dimension("1m").value == 1000
    print("test_dimensions done.")

test_dimensions()