import math


def between(b1: float, b2: float, val: float) -> bool:
    return min(b1, b2) <= val <= max(b1, b2)


def cosine_law(*, a: float = None, b: float = None, c: float = None, C: float = None) -> float:
    from sympy import var, Symbol, cos, solve
    _a, _b, _c = var('a,b,c', positive=True)
    _C = Symbol('C')
    expr = _a**2 + _b**2 - _c**2 - 2*_a*_b*cos(_C)
    solutions = solve(expr.subs({_a: a, _b: b, _c: c, _C: C}))
    return solutions[0].evalf()


def cosine_law_find_side(len1: float, len2: float, angle: float) -> float:
    return math.sqrt(len1 * len1 + len2 * len2 - 2 * len1 * len2 * math.cos(math.radians(angle)))


def cosine_law_find_angle(a: float, b: float, c: float) -> float:
    return math.degrees(math.acos((a*a + b*b - c*c) / (2 * a * b)))
