from adafruit_motor.servo import Servo
import math
import mathutils
from servo_utils import rotate, rotate2
import time


class ArmController:
    def __init__(self, *, arm1len: float, arm2len: float, arm1servo: Servo, arm2servo: Servo, tip_servo: Servo):
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
        arm1servo.angle = arm2servo.angle = 90
        tip_servo.angle = 180

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
        angle1, angle2 = self.get_angles(x, y)
        rotate2(self.arm1servo, angle1, self.arm2servo, angle2, seconds)

    def move_line(self, x0: float, y0: float, x: float, y: float, seconds: float, intervals: int) -> None:
        xVel = (x-x0)/seconds
        yVel = (y-y0)/seconds
        for i in range(1, intervals):
            rotate2(self.arm1servo, (xVel * math.cos(math.radians(self.arm1servo.angle+self.arm2servo.angle))+yVel*math.sin(math.radians(self.arm1servo.angle+self.arm2servo.angle)))/(self.arm1len*math.sin(math.radians(self.arm2servo.angle)))*seconds/intervals, self.arm2servo, (xVel * (self.arm1len * math.cos(math.radians(self.arm1servo.angle)) + self.arm2len * math.cos(math.radians(self.arm1servo.angle+self.arm2servo.angle)))+yVel * (self.arm1len * math.sin(math.radians(self.arm1servo.angle))+self.arm2len*math.sin(math.radians(self.arm1servo.angle+self.arm2servo.angle))))/(self.arm1len*self.arm2len*math.sin(math.radians(self.arm2servo.angle)))*seconds/intervals, seconds)
            time.sleep(seconds/intervals)

    def drop_tip(self) -> None:
        """Drops the tip of the pen onto the page.
        """
        self.tip_servo.angle = 180

    def lift_tip(self) -> None:
        """Lifts the tip of the pen from the page.
        """
        self.tip_servo.angle = 160

    def reset_positions(self):
        """Resets the positions of all the servos to their default position.
        The default position is both the arms perpendicular to each other and the base.
        The default position of the tip_servo connects the pen to the paper. 
        """
        self.lift_tip()
        rotate(self.arm2servo, 90)
        rotate(self.arm1servo, 90)
        time.sleep(0.2)
        self.drop_tip()
