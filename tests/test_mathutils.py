import pytest
from artificialpicasso.mathutils import between


@pytest.mark.parametrize("b1, b2, val", [
    (1, 5, 4),
    (2, 7, 2),
    (8, 4, 6),
    (0, 0, 0),
    (-3, -7, -4)
])
def test_between(b1, b2, val):
    assert between(b1, b2, val)


@pytest.mark.parametrize("b1, b2, val", [
    (1, 9, 10),
    (2, 17, -1),
    (8, 5, 0),
    (0, 0, 5),
    (-13, -7, -5)
])
def test_not_between(b1, b2, val):
    assert not between(b1, b2, val)
