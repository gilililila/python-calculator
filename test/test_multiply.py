from function.multiply import multiply


def test_multiply_positive_nums():
    assert multiply(2, 3) == 6

def test_multiply_negative_nums():
    assert multiply(-2, -3) == 6

def test_multiply_zero():
    assert multiply(0, 0) == 0
    assert multiply(0, 5) == 0

def test_multiply_mixed():
    assert multiply(-2, 3) == -6