from function.add import add


def test_add_positive_nums():
    assert add(2, 3) == 5

def test_add_negative_nums():
    assert add(-1, -3) == -4

def test_add_zero():
    assert add(0, 0) == 0

def test_add_mixed_nums():
    assert add(-2, 3) == 1
    assert add(-3, 2) == -1
    assert add(0, 5) == 5
    assert add(0, -5) == -5
