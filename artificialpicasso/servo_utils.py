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
