import cv2
import StrokeExtractor
import numpy as np


def run(image, strokeMinLength=50, speed=99):
    strokes = StrokeExtractor.getStrokes(image)

    height, width, channels = image.shape
    font = cv2.FONT_HERSHEY_SIMPLEX
    textWidth, textHeight = cv2.getTextSize('Animation finished', font, 1, 2)[0]

    speed = 101 - speed
    animate = True

    stop = False

    traceImg = 255 * np.ones(image.shape, np.uint8)

    for stroke in strokes:
        perimeter = cv2.arcLength(stroke, True)

        if perimeter >= strokeMinLength:
            points = stroke.ravel()

            if stop:
                break

            for index, point in enumerate(points):
                if index % 2 == 0:
                    x = points[index]
                    y = points[index + 1]
                    cv2.circle(image, (x, y), 2, (255, 0, 0), 1)
                    cv2.circle(traceImg, (x, y), 2, (255, 0, 0), 1)
                    cv2.imshow('image', image)

                    if animate and cv2.waitKey(speed) & 0xFF == ord('q'):
                        cv2.destroyAllWindows()
                        stop = True
                        break

    if not stop:
        cv2.putText(image, 'Animation finished', (int((width - textWidth) / 2), int((height + textHeight) / 2)), font, 1,
                    (0, 0, 255), 2)
        cv2.imshow('image', image)
    if cv2.waitKey(0) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
    return traceImg


if __name__ == "__main__":
    run(cv2.imread(input('Enter path of image to trace: ')))
