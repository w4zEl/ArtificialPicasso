"""
Captures live video stream from the camera at device index 0 (the default one).
"""

from logsetup import logger
import cv2

if __name__ == '__main__':
    cam = cv2.VideoCapture(0)
    if not cam.isOpened():
        logger.warning('Camera could not be opened')
        exit(1)
    cv2.namedWindow('Camera', cv2.WINDOW_NORMAL)
    while 1:
        ret, frame = cam.read()
        if not ret:
            logger.warning('Unable to read frame from camera')
            exit(1)
        cv2.imshow('Camera', frame)
        if cv2.waitKey(1) == ord('q'):
            break
