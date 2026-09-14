import pytest

from function.divide import divide


def test_divide_positive_nums():
    assert divide(6, 3) == 2.0

def test_divide_negative_nums():
    assert divide(-8, -4) == 2.0

def test_divide_zero():
    assert divide(0, 5) == 0.0
    with pytest.raises(ValueError, match="Division by zero is not allowed."):
        divide(5, 0)

def test_divide_mixed():
    assert divide(-9, 3) == -3.0
    assert divide(9, -3) == -3.0