from adafruit_motor.servo import Servo
import math
import mathutils
from servo_utils import rotate, rotate2
import time


class ArmController:
    def __init__(self, *, arm1len: float, arm2len: float, arm1servo: Servo, arm2servo: Servo, tip_servo: Servo):
        self.arm1len = arm1len
        self.arm2len = arm2len
        self.arm1servo = arm1servo
        self.arm2servo = arm2servo
        self.tip_servo = tip_servo
        arm1servo.angle = arm2servo.angle = 90
        tip_servo.angle = 180

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.reset_positions()
        if exc_type:
            print(exc_type, exc_val, exc_tb)

    def get_angles(self, x: float, y: float) -> tuple[float, float]:
        dist = math.hypot(x, y)
        angle1 = math.degrees(math.atan2(y, -x)) - mathutils.cosine_law_find_angle(self.arm1len, dist, self.arm2len)
        angle2 = 180 - mathutils.cosine_law_find_angle(self.arm1len, self.arm2len, dist)
        return angle1, angle2

    def move_to(self, x: float, y: float, seconds: float = 0.5) -> None:
        angle1, angle2 = self.get_angles(x, y)
        rotate2(self.arm1servo, angle1, self.arm2servo, angle2, seconds)

    def drop_tip(self) -> None:
        self.tip_servo.angle = 180

    def lift_tip(self) -> None:
        self.tip_servo.angle = 160

    def reset_positions(self):
        self.lift_tip()
        rotate(self.arm2servo, 90)
        rotate(self.arm1servo, 90)
        time.sleep(0.2)
        self.drop_tip()
