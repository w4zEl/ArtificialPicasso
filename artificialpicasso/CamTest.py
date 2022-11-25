"""
Captures live video stream from the camera at device index 0 (the default one).
"""

import cv2

cam = cv2.VideoCapture(0)
if not cam.isOpened():
    print('Camera could not be opened')
    exit(1)
cv2.namedWindow('Camera', cv2.WINDOW_NORMAL)
while 1:
    ret, frame = cam.read()
    if not ret:
        print('Unable to read frame from camera')
        exit(1)
    cv2.imshow('Camera', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
