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
            arm1len (float): The first arm of the robot
            arm2len (float): The second arm of the robot
            arm1servo (Servo): The servo connected to arm1
            arm2servo (Servo): The servo connected to arm2
            tip_servo (Servo): The servo connected to the pen
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
            exc_type (_type_): Type of the exception that occured
            exc_val (_type_): Value of the exception that occured
            exc_tb (_type_): Traceback of the exception that occured
        """
        self.reset_positions()
        if exc_type:
            print(exc_type, exc_val, exc_tb)

    def get_angles(self, x: float, y: float) -> tuple[float, float]:
        """Given a (x, y) coordinate, find the two angles that the robotic arms 
        need to make in order to move to that position.

        Args:
            x (float): The x coordinate of the target location
            y (float): The x coordinate of the target location

        Returns:
            tuple[float, float]: The angles made by arm1 and arm2 respectively 
        """
        dist = math.hypot(x, y)
        angle1 = math.degrees(math.atan2(y, -x)) - mathutils.cosine_law_find_angle(self.arm1len, dist, self.arm2len)
        angle2 = 180 - mathutils.cosine_law_find_angle(self.arm1len, self.arm2len, dist)
        return angle1, angle2

    def move_to(self, x: float, y: float, seconds: float = 0.5) -> None:
        """Given a (x, y) coordinate and a specified time, moves the robotic arm 
        to the desired coordinate within that exact time frame.

        Args:
            x (float): The x coordinate of the target location (Left is positive)
            y (float): The y coordinate of the target location (Up is positive)
            seconds (float, optional): The time taken to get to the location. Defaults to 0.5.
        """
        angle1, angle2 = self.get_angles(x, y)
        rotate2(self.arm1servo, angle1, self.arm2servo, angle2, seconds)

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
