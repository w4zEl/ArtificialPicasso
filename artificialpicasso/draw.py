from arm import ArmController, Paper
from servo_utils import make_servo, make_adjusted_servo
import cv2
import StrokeExtractor

with ArmController(arm1len=20.2, arm2len=22.1,
                   arm1servo=make_adjusted_servo(3, convert_angle=lambda x: 180 - x, max_pulse=2500),
                   arm2servo=make_adjusted_servo(1, convert_angle=lambda x: 180 - x, max_pulse=2500),
                   tip_servo=make_servo(0), paper=Paper(3.5, 3.5, 27.6, 21.3)) as controller:
    img = cv2.imread(input('Image path: '))
    strokes = StrokeExtractor.getStrokes(img, 5)
    strokeMinLength = 50
    armStrokeLen = 20
    height, width, *_ = img.shape

    def scale_to_paper(x, y):
        return (1 - x / width) * controller.paper.width, (1 - y / height) * controller.paper.height

    for stroke in strokes:
        controller.lift_tip()
        perimeter = cv2.arcLength(stroke, True)

        if perimeter >= strokeMinLength:
            points = stroke.ravel()
            index = 0
            numOfPoints = len(points)

            lastX, lastY = None, None
            for point in points:
                if index < numOfPoints and index % 2 == 0:
                    x = points[index]
                    y = points[index + 1]
                    if lastX is not None and lastY is not None:
                        controller.line(*scale_to_paper(lastX, lastY), *scale_to_paper(x, y))
                    lastX = x
                    lastY = y
                index = index + armStrokeLen * 2
    input('Press enter to terminate.')
