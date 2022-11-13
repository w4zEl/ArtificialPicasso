from arm import ArmController
from servo_utils import make_servo
import time

# lengths are in cm, but any unit is fine as long as they are all consistent
paper_delta_x = paper_delta_y = 3.5
paper_width = 27.6
paper_height = 21.3
controller = ArmController(arm1len=20, arm2len=22.3, arm1servo=make_servo(5), arm2servo=make_servo(0),
                           tip_servo=make_servo(1))
