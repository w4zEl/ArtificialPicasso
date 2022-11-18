import numpy as np


def filled_image(dimensions: tuple[int, int, int], color: int) -> np.ndarray:
    return np.full(dimensions, color, np.uint8)


def white_image(dimensions: tuple[int, int, int]) -> np.ndarray:
    return filled_image(dimensions, 255)
