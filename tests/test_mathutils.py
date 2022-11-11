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
