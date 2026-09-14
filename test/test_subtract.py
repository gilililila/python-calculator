from function.subtract import subtract


def test_subtract_positive():
    assert subtract(5, 3) == 2


def test_subtract_negative():
    assert subtract(-1, -1) == 0


def test_subtract_zero():
    assert subtract(0, 0) == 0

def test_subtract_mixed():
    assert subtract(5, -3) == 8
    assert subtract(-5, 3) == -8
    assert subtract(0, -3) == 3
    assert subtract(-3, 0) == -3