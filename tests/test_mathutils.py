import pytest
from artificialpicasso.mathutils import between, cosine_law_find_angle, cosine_law_find_side


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

@pytest.mark.parametrize("a, b, c, angle", [
    (3, 4, 5, 90),
    (5, 8, 9, 84.26082952273322),
    (7.5, 6.5, 3.5, 27.795772496027972), 
    (1, 1.414, 1, 45.008651662837984),
    (10, 4, 6, 0)
])
def test_cosine_law_find_angle(a, b, c, angle): 
    assert abs(cosine_law_find_angle(a, b, c) - angle) < 0.000001

@pytest.mark.parametrize("a, b, c, angle", [
    (6, 7, 9, 90),
    (68, 20, 85, 140),
    (17.5, 20, 5, 14), 
    (2, 3, 4, 100), 
    (22, 66, 44, 1)
])
def test_not_cosine_law_find_angle(a, b, c, angle): 
    assert not abs(cosine_law_find_angle(a, b, c) - angle) < 0.000001

@pytest.mark.parametrize("a, b, angle, side_found", [
    (15, 16, 2.5, 1.2070019224128155), 
    (20, 40, 1, 20.006091266156265),
    (3, 4, 90, 5), 
    (15, 35.5, 50, 28.296310637322236), 
    (4.5, 6.5, 179, 10.999595000119273)
])

def test_cosine_law_find_side(a, b, angle, side_found): 
    assert abs(cosine_law_find_side(a, b, angle) - side_found) < 0.000001

@pytest.mark.parametrize("a, b, angle, side_found", [
    (6, 7, 10.5, 1),
    (2, 4, 90, 4), 
    (69, 420, 0.1, 350), 
    (2.5, 8.55, 120, 20),
    (60, 30, 15, 29)
])

def test_not_cosine_law_find_side(a, b, angle, side_found): 
    assert not abs(cosine_law_find_side(a, b, angle) - side_found) < 0.000001
    