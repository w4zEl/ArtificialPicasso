import numpy as np
import cv2
from PIL import Image, ImageTk


def filled_image(dimensions: tuple[int, int, int], color: int) -> np.ndarray:
    return np.full(dimensions, color, np.uint8)


def white_image(dimensions: tuple[int, int, int]) -> np.ndarray:
    return filled_image(dimensions, 255)


def cv2_image_to_image_tk(img):
    return ImageTk.PhotoImage(Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGBA)))
