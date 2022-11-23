import cv2
import StrokeExtractor
import imgutils


def run(image, strokeminlength=50, speed=99, edgeSensitivity = 5):
    strokes = StrokeExtractor.getStrokes(image, edgeSensitivity)

    height, width, channels = image.shape
    font = cv2.FONT_HERSHEY_SIMPLEX
    text_width, text_height = cv2.getTextSize('Animation finished', font, 1, 2)[0]

    speed = 101 - speed
    animate = True

    stop = False

    trace_img = imgutils.white_image(image.shape)

    for stroke in strokes:
        perimeter = cv2.arcLength(stroke, True)

        if perimeter >= strokeminlength:
            points = stroke.ravel()

            if stop:
                break

            for index, point in enumerate(points):
                if index % 2 == 0:
                    x = points[index]
                    y = points[index + 1]
                    cv2.circle(image, (x, y), 2, (255, 0, 0), 1)
                    cv2.circle(trace_img, (x, y), 2, (255, 0, 0), 1)
                    cv2.imshow('image', image)

                    if animate and cv2.waitKey(speed) & 0xFF == ord('q'):
                        cv2.destroyAllWindows()
                        stop = True
                        break

    if not stop:
        cv2.putText(image, 'Animation finished', (int((width - text_width) / 2), int((height + text_height) / 2)), font, 1,
                    (0, 0, 255), 2)
        cv2.imshow('image', image)
    if cv2.waitKey(0) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
    return trace_img


if __name__ == "__main__":
    run(cv2.imread(input('Enter path of image to trace: ')))
