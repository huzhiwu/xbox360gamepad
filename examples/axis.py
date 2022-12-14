import time
import logging; logging.basicConfig(level=logging.DEBUG)

from xbox360gamepad import GamepadController

controller = GamepadController()


# single axis
def on_abs_l_move(obj):
    print(f'{obj.name}: x:{obj.x}, y:{obj.y}, z:{obj.z}')

controller.axis_l.on_move = on_abs_l_move


# all
def on_abs_move(obj):
    print(f'{obj.name}: x:{obj.x}, y:{obj.y}, z:{obj.z}')

controller.hat.on_move = on_abs_move
controller.axis_l.on_move = on_abs_move
controller.axis_r.on_move = on_abs_move
controller.trigger_l.on_move = on_abs_move
controller.trigger_r.on_move = on_abs_move


if __name__ == '__main__':
    try:
        controller.start()
        while 1:
            # your codes
            time.sleep(1)
    except KeyboardInterrupt:
        controller.close()
