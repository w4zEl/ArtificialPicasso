from adafruit_pca9685 import PCA9685
from adafruit_motor.servo import Servo
import board
import time
import atexit
from typing import Callable, Optional
from math import inf
from loguru import logger

pca = PCA9685(board.I2C())
pca.frequency = 50
min_pulse, max_pulse = 500, 2600


def make_servo(channel: int) -> Servo:
    """Initialize the servos
    """
    return Servo(pca.channels[channel], min_pulse=min_pulse, max_pulse=max_pulse)


def make_adjusted_servo(channel: int, **kwargs) -> Servo:
    return ServoWrapper(pca.channels[channel], min_pulse=kwargs.pop('min_pulse', min_pulse),
                        max_pulse=kwargs.pop('max_pulse', max_pulse), **kwargs)


class ServoWrapper(Servo):
    def __init__(self, *args, convert_angle: Optional[Callable[[float], float]] = None,
                 reverse_convert: Optional[Callable[[float], float]] = None,
                 max_angle_delta: float = inf,
                 **kwargs):
        self.convert_angle = convert_angle
        self.reverse_convert = reverse_convert or convert_angle
        if bool(self.convert_angle) != bool(self.reverse_convert):
            logger.warning('Only one conversion function given. '
                           'It is recommended to provide both so the conversion can be reversed.')
        self.max_angle_delta = max_angle_delta
        super().__init__(*args, **kwargs)

    @property
    def angle(self) -> Optional[float]:
        a = super().angle
        return self.reverse_convert(a) if a and self.reverse_convert else a

    @angle.setter
    def angle(self, new_angle: Optional[int]) -> None:
        if new_angle and abs(self.angle - new_angle) > self.max_angle_delta:
            logger.warning(f'Stopped attempt to rotate more than allowed max_angle_delta [{self.max_angle_delta}] at '
                           f'once! Current angle: {self.angle}, new_angle: {new_angle}')
            return
        super(__class__, self.__class__).angle.__set__(self, self.convert_angle(new_angle)
                                                       if new_angle and self.convert_angle else new_angle)


@atexit.register
def cleanup() -> None:
    pca.deinit()


def rotate(s: Servo, angle: float, seconds: float = 0.5, increment: float = 1) -> None:
    """Rotates the given servo to the desired angle in the desired amount of time.

    Args:
        s (Servo): The servo to rotate 
        angle (float): The angle in degrees to rotate. 0 <= angle <= 180
        seconds (float, optional): Time in seconds to rotate the arm in. Defaults to 0.5.
        increment (float, optional): Moves the arm in increments of this size in degrees. Defaults to 1 degree.
    """
    delay = seconds / (abs(angle - s.angle) / increment)
    delta = increment if s.angle < angle else -increment
    cap = min if s.angle < angle else max
    while abs(s.angle - angle) > .5:
        s.angle = cap(s.angle + delta, angle)
        time.sleep(delay)


def increment(angle, delta, target):
    return angle + delta if angle + delta < target else angle - delta if angle - delta > target else target


def rotate2(servo1: Servo, angle1: float, servo2: Servo, angle2: float, seconds: float = 0.5) -> None:
    """
    Rotate two servos simultaneously to reach the desired angle for each in the same amount of time
    """
    if seconds < 0:
        raise ValueError("seconds cannot be negative")
    if seconds == 0:
        servo1.angle, servo2.angle = angle1, angle2
        return
    if abs(servo1.angle - angle1) > abs(servo2.angle - angle2):
        servo1, angle1, servo2, angle2 = servo2, angle2, servo1, angle1
    increment1 = 1
    rotations = abs(servo1.angle - angle1) / increment1
    delay1 = seconds / rotations
    increment2 = abs(servo2.angle - angle2) / rotations
    curr_angle1 = servo1.angle
    curr_angle2 = servo2.angle

    while abs(servo1.angle - angle1) > .5:
        servo1.angle = curr_angle1 = increment(curr_angle1, increment1, angle1)
        servo2.angle = curr_angle2 = increment(curr_angle2, increment2, angle2)
        time.sleep(delay1)
    servo1.angle = angle1
    servo2.angle = angle2


def safe_rotate(s: Servo, angle: float, delay: float = 0.03) -> None:
    if delay <= 0:
        raise ValueError("delay must be positive")
    if s.angle < angle:
        while s.angle + 1 < angle:
            s.angle += 1
            time.sleep(delay)
        s.angle = angle
    else:
        while s.angle - 1 > angle:
            s.angle -= 1
            time.sleep(delay)
        s.angle = angle

def rotate3(servo1: Servo, angle1: float, servo2: Servo, angle2: float, increment: float, seconds: float = 0.5) -> None:
    counter = increment
    increment1 = (angle1-servo1.angle)/(seconds/increment)
    increment2 = (angle2-servo2.angle)/(seconds/increment)
    curr_angle1 = servo1.angle
    curr_angle2 = servo2.angle
    while counter<seconds:
        servo1.angle = curr_angle1+increment1
        servo2.angle = curr_angle2+increment2
        curr_angle1 = servo1.angle
        curr_angle2 = servo2.angle
        counter += increment
        time.sleep (increment)
    servo1.angle = angle1
    servo2.angle = angle2