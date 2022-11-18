from adafruit_pca9685 import PCA9685
from adafruit_motor.servo import Servo
import board
import time
import atexit

pca = PCA9685(board.I2C())
pca.frequency = 50
min_pulse, max_pulse = 500, 2600


def make_servo(channel: int) -> Servo:
    return Servo(pca.channels[channel], min_pulse=min_pulse, max_pulse=max_pulse)


@atexit.register
def cleanup() -> None:
    pca.deinit()


def rotate(s: Servo, angle: float, seconds: float = 0.5, increment: float = 1) -> None:
    delay = seconds / (abs(angle - s.angle) / increment)
    delta = increment if s.angle < angle else -increment
    cap = min if s.angle < angle else max
    while abs(s.angle - angle) > .5:
        s.angle = cap(s.angle + delta, angle)
        time.sleep(delay)


def rotate2(servo1: Servo, angle1: float, servo2: Servo, angle2: float, seconds: float = 0.5) -> None:
    """
    Rotate two servos simultaneously to reach the desired angle for each in the same amount of time
    """
    if abs(servo1.angle - angle1) < abs(servo2.angle - angle2):
        servo1, angle1, servo2, angle2 = servo2, angle2, servo1, angle1
    rotations = abs(servo1.angle - angle1)
    delay1 = seconds / rotations
    increment2 = abs(servo2.angle - angle2) / rotations
    curr_angle1 = servo1.angle
    curr_angle2 = servo2.angle

    def increment(angle, delta, target):
        return angle + delta if angle + delta < target else angle - delta if angle - delta > target else target
    while abs(servo1.angle - angle1) > .5:
        servo1.angle = curr_angle1 = increment(curr_angle1, 1, angle1)
        servo2.angle = curr_angle2 = increment(curr_angle2, increment2, angle2)
        time.sleep(delay1)
