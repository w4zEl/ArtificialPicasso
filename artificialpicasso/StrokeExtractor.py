import cv2

def getStrokes(image):
    """Generates the strokes of the image that need to be drawn.

    Uses canny edge detection and other contour-finding algorithms 
    in Open CV to generate the strokes of the image. 

    Args:
        image (np.ndarray): A 3-d list of pixels that represent an image

    Returns:
        _type_: Returns a list of all the strokes of the image
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 1, 50)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,3))
    edges = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)
    contours = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    contours = contours[0] if len(contours) == 2 else contours[1]
    return contours
