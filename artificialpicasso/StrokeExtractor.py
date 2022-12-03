import cv2


def blur(image, edgeSensitivity):
    edgeSensitivity = 10 - edgeSensitivity
    edgeSensitivity *= 2
    edgeSensitivity += 1
    grey_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    invert = cv2.bitwise_not(grey_img)
    blur = cv2.GaussianBlur(invert, (21, 21), 0)
    invertedblur = cv2.bitwise_not(blur)
    sketch = cv2.divide(grey_img, invertedblur, scale=256.0)
    blurredsketch = cv2.GaussianBlur(sketch, (edgeSensitivity, edgeSensitivity), 0)
    return blurredsketch


def getStrokes(image, blur=True):
    """Generates the strokes of the image that need to be drawn.

    Uses canny edge detection and other contour-finding algorithms 
    in Open CV to generate the strokes of the image. 

    Args:
        image (np.ndarray): A 3-d list of pixels that represent an image

    Returns:
        _type_: Returns a list of all the strokes of the image
    """
    # gray = blur(image, edgeSensitivity)
    gray = cv2.cvtColor(cv2.GaussianBlur(image, (3, 3), 0), cv2.COLOR_BGR2GRAY)
    if blur:
        gray = cv2.GaussianBlur(gray, (3, 3), 0)
    edges = cv2.Canny(gray, 1, 50)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    edges = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)
    contours = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    contours = contours[0] if len(contours) == 2 else contours[1]
    return contours
