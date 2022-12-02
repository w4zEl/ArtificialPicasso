"""
Takes a picture from a camera.
"""

from logsetup import logger
import cv2
from argparse import ArgumentParser
from datetime import datetime

if __name__ == '__main__':
    parser = ArgumentParser(description='Takes a picture.')
    parser.add_argument('-o', '--output', help='Output file',
                        default=f"img_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.png")
    parser.add_argument('-i', '--cam-index', help='The device index of the camera to use', default=0)
    args = parser.parse_args()
    cam = cv2.VideoCapture(args.cam_index)

    if not cam.isOpened():
        logger.warning('Camera could not be opened')
        exit(1)
    ret, img = cam.read()
    if not ret:
        logger.warning('Could not read frame from camera')
        exit(1)
    cv2.imwrite(args.output, img)
    logger.info('Successfully saved picture to {}', args.output)
