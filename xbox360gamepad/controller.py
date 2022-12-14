import threading
import logging
import time
import importlib

import inputs


class EVENT_TYPE:
    BUTTON = 'Key'
    AXIS = 'Absolute'


class Axis:
    def __init__(self, name):
        self.name = name
        self.__x = 0
        self.__y = 0
        self.__z = 0    # only for trigger_l, trigger_r
        self.on_move = None

    @property
    def x(self):
        return self.__x

    @x.setter
    def x(self, v):
        self.__x = v
        self.run_on_move()

    @property
    def y(self):
        return self.__y

    @y.setter
    def y(self, v):
        self.__y = v
        self.run_on_move()

    @property
    def z(self):
        return self.__z

    @z.setter
    def z(self, v):
        self.__z = v
        self.run_on_move()

    def run_on_move(self):
        if callable(self.on_move):
            self.on_move(self)


class Button:
    def __init__(self, name):
        self.name = name
        self.__value = False
        self.on_up = None
        self.on_down = None

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, v):
        self.__value = v
        if self.__value and callable(self.on_down):
            self.on_down(self)
        if not self.__value and callable(self.on_up):
            self.on_up(self)

    @property
    def is_pressed(self):
        return bool(self._value)


class GamepadController:
    def __init__(self):
        self._event_thread_stopped = None
        self._gamepad_connected = False
        self._gamepad = None

        self.button_select = Button("button_select")
        self.button_start = Button("button_start")
        self.button_mode = Button("button_mode")
        self.button_a = Button("button_a")
        self.button_b = Button("button_b")
        self.button_x = Button("button_x")
        self.button_y = Button("button_y")
        self.button_trigger_l = Button("button_trigger_l")
        self.button_trigger_r = Button("button_trigger_r")
        self.button_thumb_l = Button("button_thumb_l")
        self.button_thumb_r = Button("button_thumb_r")
        self.buttons = {
            "BTN_SELECT": self.button_select,
            "BTN_START": self.button_start,
            "BTN_MODE": self.button_mode,
            "BTN_SOUTH": self.button_a,
            "BTN_EAST": self.button_b,
            "BTN_NORTH": self.button_x,
            "BTN_WEST": self.button_y,
            "BTN_TL": self.button_trigger_l,
            "BTN_TR": self.button_trigger_r,
            "BTN_THUMBL": self.button_thumb_l,
            "BTN_THUMBR": self.button_thumb_r,
        }
        self.axis_l = Axis("axis_l")
        self.axis_r = Axis("axis_r")
        self.hat = Axis("hat")
        self.trigger_l = Axis('trigger_l')
        self.trigger_r = Axis('trigger_r')

    @property
    def gamepad(self):
        if not self._gamepad or not self._gamepad_connected:
            self._gamepad = self._get_gamepad()
            logging.info(f"Gamepad connected:{self._gamepad}")
            self._gamepad_connected = True

        return self._gamepad

    def _get_gamepad(self):
        try:
            if not self._gamepad_connected:
                importlib.reload(inputs)
            return inputs.devices.gamepads[0]
        except IndexError:
            logging.warning("No gamepad found. Waiting device to connect...")
            time.sleep(1)
            self._get_gamepad()

    def _event_loop(self):
        while not self._event_thread_stopped.is_set():
            self.process_events()
        logging.info('exit event loop')

    def start(self):
        self._event_thread_stopped = threading.Event()
        self._event_thread = threading.Thread(target=self._event_loop)
        self._event_thread.start()

    def close(self):
        logging.info('close')
        self._event_thread_stopped.set()
        self._event_thread.join()

    def process_events(self):
        events = []
        try:
            if self.gamepad and self._gamepad_connected:
                events = self.gamepad.read()
        except (EOFError, ):
            pass
        except OSError:
            self._gamepad_connected = False
        for event in events:
            self.process_event(event)

    def process_event(self, event):
 #       logging.debug(f"{event.ev_type}, {event.code}, {event.state}")

        if event.ev_type == EVENT_TYPE.BUTTON:
            button = self.buttons.get(event.code)
            if button:
                button.value = event.state

        if event.ev_type == EVENT_TYPE.AXIS:
            if event.code == 'ABS_HAT0X':
                self.hat.x = event.state
            elif event.code == 'ABS_HAT0Y':
                self.hat.y = event.state
            elif event.code == 'ABS_X':
                self.axis_l.x = event.state / 32767
            elif event.code == 'ABS_Y':
                # 这里inputs库似乎有个bug，摇杆y不归0
                self.axis_l.y = 0 if event.state == -1 else event.state / 32767
            elif event.code == 'ABS_RX':
                self.axis_r.x = event.state / 32767
            elif event.code == 'ABS_RY':
                self.axis_r.y = 0 if event.state == -1 else event.state /32767
            elif event.code == 'ABS_Z':
                self.trigger_l.z = event.state
            elif event.code == 'ABS_RZ':
                self.trigger_r.z = event.state
