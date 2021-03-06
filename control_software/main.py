"""
  Basic imports and defaults.
"""
from joystick_controller import *
import os
from pprint import pprint
import numpy as np
import math


from robot_model import *
"""
  Process related imports.
"""


def _map(x, in_min, in_max, out_min, out_max) -> int:
    return int((x-in_min) * (out_max - out_min) / (in_max - in_min) + out_min)


if __name__ == "__main__":
    ps4: PS4Controller = PS4Controller()
    ps4.init()

    toggle_debug: bool = True
    translateMode: bool = False
    rotateMode: bool = False

    axis: str = "y"

    while True:
        robot: RobotModel = RobotModel("192.168.0.125", 80, True, 1)

        os.system("clear")
        inputs: dict = (ps4.listen())
        print("Debug: " + str(toggle_debug))
        print("Translate Mode: " + str(translateMode))
        if translateMode:
            print("Axis: " + str(axis))

        print("Rotate Mode: " + str(rotateMode))
        if rotateMode:
            print("Axis: " + str(axis))

        if inputs["right"]:
          robot.mode = 3 
          robot.reload()


        if inputs["option"]:
            toggle_debug = not toggle_debug

        if toggle_debug:
            pprint(inputs)

        if inputs["home"]:
            print("Closing goodbye!")
            break

        if inputs["r1"]:
            print("Rotating")
            robot.trotRotate2(direction=1)
            # robot.trotTraverse(direction=1)

        if inputs["r2"]:
            robot.trotTraverse(direction=1)

        if inputs["l2"]:
            robot.trotTraverse(direction=0)

        if inputs["l1"]:
            print("Rotating")
            robot.trotRotate2(direction=0)

        if inputs["s"] == 1 and not inputs["o"] == 1:
            print("Toggling Translate Mode")
            translateMode = not translateMode

        if inputs["o"] == 1 and not inputs["s"] == 1:
            print("Toggling Rotate Mode")
            rotateMode = not rotateMode

        if rotateMode:
            if inputs["x"] == 1:
                axis = "x"
            elif inputs["t"] == 1:
                axis = "y"
            try:
                robot.rotate(inputs["left_y"], inputs["left_x"],
                             inputs["right_y"], axis=axis)
                print(robot.leg_1.show())
                print(robot.leg_2.show())
                print(robot.leg_3.show())
                print(robot.leg_4.show())
                robot.reload()
            except KeyError as e:
                print("Roll Sticks")

        if inputs["pad"] == True:
            robot.restart()

        if translateMode:
            if inputs["x"] == 1:
                axis = "x"
            elif inputs["t"] == 1:
                axis = "y"
            try:
                robot.translate(inputs['left_x'],
                                inputs['left_y'], inputs['right_y'], axis=axis)

                #robot.leg_1.x = _map(inputs["right_y"], -1, 1, 1, 100)
                #robot.leg_2.x = _map(inputs["right_x"], -1, 1, 1, 100)
                #robot.increment = _map(inputs["left_y"], -1, 1, -30, 30)

                robot.reload()
                print(robot.leg_1.show())
                print(robot.leg_2.show())
                print(robot.leg_3.show())
                print(robot.leg_4.show())

            except KeyError as e:
                print("Roll Sticks")

        # newLoad = robot.newPayload
        # robot.sendLoad(bytearray(newLoad))
