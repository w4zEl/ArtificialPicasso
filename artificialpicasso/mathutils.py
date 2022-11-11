def between(b1: float, b2: float, val: float) -> bool:
    return min(b1, b2) <= val <= max(b1, b2)
