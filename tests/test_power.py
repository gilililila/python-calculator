from calculator import power


def test_power_positive_nums():
    assert power(2, 3) == 8

def test_power_zero_exp():
    assert power(5, 0) == 1
    assert power(0, 0) == 1

def test_power_one():
    assert power(5, 1) == 5
