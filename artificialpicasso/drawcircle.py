import math
from arm import ArmController
from servo_utils import *


def drawcircle(x: float, y: float, radius: float, segments: int) -> None:
    controller.lift_tip()
    controller.move_to(x + paper_delta_x + radius, y + paper_delta_y)
    controller.drop_tip()
    for i in range(0, segments + 1):
        controller.move_to(x + paper_delta_x + radius * math.cos(2 * math.pi * i / segments),
                           y + paper_delta_y + radius * math.sin(2 * math.pi * i / segments))


if __name__ == '__main__':
    paper_delta_x = paper_delta_y = 3.5
    controller = ArmController(arm1len=20.2, arm2len=22.1,
                               arm1servo=make_adjusted_servo(3, convert_angle=lambda x: 180 - x, max_pulse=2500),
                               arm2servo=make_adjusted_servo(1, convert_angle=lambda x: 180 - x, max_pulse=2500),
                               tip_servo=make_servo(0))
    drawcircle(15, 15, 5, 50)
