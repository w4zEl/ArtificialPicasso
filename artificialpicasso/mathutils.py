import math


def between(b1: float, b2: float, val: float) -> bool:
    """Returns true if val is a number between b1 and b2 (inclusive). 

    Args:
        b1 (float): Lower bound
        b2 (float): Upper bound
        val (float): The number being checked

    Returns:
        bool: True if val is in between b1 and b2 (inclusive), false otherwise. 
    """
    return min(b1, b2) <= val <= max(b1, b2)


def cosine_law(*, a: float = None, b: float = None, c: float = None, C: float = None) -> float:
    """Solves a triangle using cosine law. 

    If given all 3 side lengths of a triangle, returns the angle opposite to side c. 
    If given the lengths of 2 sides of a trianle and the angle opposite to side c,
    returns the length of the missing side. 

    Args:
        a (float, optional): Length of the first side of the triangle. Defaults to None.
        b (float, optional): Length of the second side. Defaults to None.
        c (float, optional): Length of the third side. Defaults to None.
        C (float, optional): The angle opposite to side c (in degrees). Defaults to None.

    Returns:
        float: The value of the missing argument
    """

    from sympy import var, Symbol, cos, solve
    _a, _b, _c = var('a,b,c', positive=True)
    _C = Symbol('C')
    expr = _a**2 + _b**2 - _c**2 - 2*_a*_b*cos(_C)
    solutions = solve(expr.subs({_a: a, _b: b, _c: c, _C: C}))
    return solutions[0].evalf()


def cosine_law_find_side(len1: float, len2: float, angle: float) -> float:
    """Given 2 side lengths of a triangle and the angle in between (in degrees),
    finds the length of the 3rd side. 

    Args:
        len1 (float): Length of the first side of a triangle
        len2 (float): Length of the second side of a triangle
        angle (float): Angle (in degrees) between len1 and len2

    Returns:
        float: Length of the 3rd side of the triangle given
    """
    return math.sqrt(len1 * len1 + len2 * len2 - 2 * len1 * len2 * math.cos(math.radians(angle)))


def cosine_law_find_angle(a: float, b: float, c: float) -> float:
    """Given 3 side lengths of a triangle, find the angle opposite to one of the sides (side c).

    Args:
        a (float): First side length of a traingle
        b (float): Second side length of a triangle
        c (float): Third side length of a triangle

    Returns:
        float: The angle opposite to c, in degrees. 
    """
    return math.degrees(math.acos((a*a + b*b - c*c) / (2 * a * b)))
