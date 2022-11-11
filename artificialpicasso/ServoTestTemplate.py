"""
Used for quick interactive servo testing on the Raspberry Pi with I2C PCA9685
e.g. by running:

python -i ServoTestTemplate.py
"""

import time
import board
from adafruit_motor import servo
from adafruit_pca9685 import PCA9685

pca = PCA9685(board.I2C())
pca.frequency = 50

min_pulse = 500
max_pulse = 2600
makeServo = lambda channel: servo.Servo(pca.channels[channel], min_pulse=min_pulse, max_pulse=max_pulse)


def rotate(s: servo, angle: float, ms: float, increment: float = 1) -> None:
    delay = ms / (abs(angle - s.angle) / increment)
    print(delay)
    delta = increment if s.angle < angle else -increment
    cap = min if s.angle < angle else max
    while abs(s.angle - angle) > .5:
        s.angle = cap(s.angle + delta, angle)
        print('rotate to', s.angle)
        time.sleep(delay / 1000)


def stop():
    pca.deinit()
    exit()
