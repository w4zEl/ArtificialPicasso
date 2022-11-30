"""
Convenient template for testing arm movements. In interactive mode, DO NOT stop the program with Ctrl + Z;
otherwise, the arm will not reset to the default positions properly. Use Ctrl + D or exit() instead.
"""
from arm import ArmController
from servo_utils import make_servo, make_adjusted_servo
import time
import atexit

if __name__ == '__main__':
    # lengths are in cm, but any unit is fine as long as they are all consistent
    paper_delta_x = paper_delta_y = 3.5
    paper_width = 27.6
    paper_height = 21.3
    controller = ArmController(arm1len=20, arm2len=22.3, arm1servo=make_adjusted_servo(3, lambda x: 180 - x),
                               arm2servo=make_servo(1), tip_servo=make_servo(0))
    atexit.register(controller.reset_positions)


def move_to_paper_coords(x: float, y: float, *rest) -> None:
    controller.move_to(x + paper_delta_x, y + paper_delta_y, *rest)
