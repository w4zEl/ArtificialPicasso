import math
import mathutils
from adafruit_motor.servo import Servo
from servo_utils import rotate, rotate2, rotateee, safe_rotate, increment, rotate2_incremental
import time
from dataclasses import dataclass
from typing import Optional


@dataclass
class Paper:
    """Value object to store attributes about the paper used for drawing"""
    delta_x: float
    delta_y: float
    width: float
    height: float


class ArmController:
    def __init__(self, *, arm1len: float, arm2len: float, arm1servo: Servo, arm2servo: Servo, tip_servo: Servo,
                 autosetpos: bool = True, paper: Optional[Paper] = None):
        """Initializes all the different components of the robot, as well as their positions. 

        The default position of the arms are them perpendicular to each other and the base.
        The default position of the tip_servo connects the pen to the paper.

        Args:
            arm1len: The first arm of the robot
            arm2len: The second arm of the robot
            arm1servo: The servo connected to arm1
            arm2servo: The servo connected to arm2
            tip_servo: The servo connected to the pen
        """
        self.arm1len = arm1len
        self.arm2len = arm2len
        self.arm1servo = arm1servo
        self.arm2servo = arm2servo
        self.tip_servo = tip_servo
        self.autosetpos = autosetpos
        self.paper = paper
        if autosetpos:
            arm1servo.angle = arm2servo.angle = 90
            tip_servo.angle = 170

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Resets the arm after execution is terminated,
        either after completion of execution or in the event of an exception. 

        Args:
            exc_type: Type of the exception that occurred
            exc_val: Value of the exception that occurred
            exc_tb: Traceback of the exception that occurred
        """
        self.reset_positions()

    def get_angles(self, x: float, y: float) -> tuple[float, float]:
        """Given a (x, y) coordinate, find the two angles that the robotic arms 
        need to make in order to move to that position.

        Args:
            x: The x coordinate of the target location
            y: The x coordinate of the target location

        Returns:
            The angles made by arm1 and arm2, respectively.
        """
        dist = math.hypot(x, y)
        angle1 = math.degrees(math.atan2(y, -x)) - mathutils.cosine_law_find_angle(self.arm1len, dist, self.arm2len)
        angle2 = 180 - mathutils.cosine_law_find_angle(self.arm1len, self.arm2len, dist)
        return angle1, angle2

    def move_to(self, x: float, y: float, seconds: float = 0.5) -> None:
        """Given a (x, y) coordinate and a specified time, moves the robotic arm 
        to the desired coordinate within that exact time frame.

        Args:
            x: The x coordinate of the target location (Left is positive)
            y: The y coordinate of the target location (Up is positive)
            seconds: The time taken to get to the location.
        """
        if self.paper:
            x += self.paper.delta_x
            y += self.paper.delta_y
        angle1, angle2 = self.get_angles(x, y)
        rotate2_incremental(self.arm1servo, angle1, self.arm2servo, angle2)

    def line(self, x1: float, y1: float, x2: float, y2: float, segment_len: float = 0.5, drop: bool = True) -> None:
        self.move_to(x1, y1)
        if drop:
            self.drop_tip()
        dist = math.hypot(x2 - x1, y2 - y1)
        x, y = x1, y1
        segments = math.ceil(dist / segment_len)
        rise = abs(y2 - y1) / segments
        run = abs(x2 - x1) / segments
        while x != x2:
            self.move_to(x := increment(x, run, x2), y := increment(y, rise, y2))

    def drop_tip(self) -> None:
        """Drops the tip of the pen onto the page.
        """
        self.tip_servo.angle = 180

    def lift_tip(self) -> None:
        """Lifts the tip of the pen from the page.
        """
        self.tip_servo.angle = 170

    def reset_positions(self):
        """Resets the positions of all the servos to their default position.
        The default position is both the arms perpendicular to each other and the base.
        The default position of the tip_servo connects the pen to the paper. 
        """
        if self.autosetpos:
            self.lift_tip()
            safe_rotate(self.arm2servo, 90)
            safe_rotate(self.arm1servo, 90)
