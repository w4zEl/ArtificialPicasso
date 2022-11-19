"""
Used for quick interactive servo testing on the Raspberry Pi with I2C PCA9685.

For example, by running:

.. code-block::

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


def rotate(s: servo.Servo, angle: float, ms: float, increment: float = 1) -> None:
    """Rotates the given servo to the desired angle in the desired amount of time.

    Args:
        s: The servo to rotate
        angle: The angle in degrees to rotate. 0 <= angle <= 180
        ms: Time in milliseconds to rotate the arm in.
        increment: Moves the arm in increments of this size in degrees. Defaults to 1 degree.
    """
    delay = ms / (abs(angle - s.angle) / increment)
    print(delay)
    delta = increment if s.angle < angle else -increment
    cap = min if s.angle < angle else max
    while abs(s.angle - angle) > .5:
        s.angle = cap(s.angle + delta, angle)
        print('rotate to', s.angle)
        time.sleep(delay / 1000)


def stop():
    """Releases usage of the PCA and exits"""
    pca.deinit()
    exit()
