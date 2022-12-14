import time
import logging; logging.basicConfig(level=logging.DEBUG)

from xbox360gamepad import GamepadController

controller = GamepadController()


# single button
def on_a_up(obj):
    print(f"Btn A: {obj.value}")

def on_a_down(obj):
    print(f"Btn A: {obj.value}")

def on_x_up(obj):
    print(f"Btn A: {obj.value}")

def on_x_down(obj):
    print(f"Btn A: {obj.value}")

controller.button_a.on_up = on_a_up
controller.button_a.on_down = on_a_down
controller.button_x.on_up = on_x_up
controller.button_x.on_down = on_x_down


# all buttons
def on_button_down(obj):
    print(f'{obj.name}:{obj.value}')

def on_button_up(obj):
    print(f'{obj.name}:{obj.value}')


for k, v in controller.buttons.items():
    v.on_up = on_button_up
    v.on_down = on_button_down


if __name__ == '__main__':
    try:
        controller.start()
        while 1:
            # your codes
            time.sleep(1)
    except KeyboardInterrupt:
        controller.close()
