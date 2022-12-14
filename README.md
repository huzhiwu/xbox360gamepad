xbox360gamepad
==============

A x360 box gamepad controller API

为了方便小孩子捣鼓树莓派小车，机器人等等，从淘宝购买的无限手柄🎮，店家未提供驱动和开发库。所以基于inputs库简单封装了一下。


Installation
------------
```sh
pip3 install https://github.com/huzhiwu/xbox360gamepad
```

Usage
-----

```python
import time
from xbox360gamepad import GamepadController

controller = GamepadController()

# 按钮

def on_a_up(obj):
    print(f"Btn A: {obj.value}")

def on_a_down(obj):
    print(f"Btn A: {obj.value}")

controller.button_a.on_up = on_a_up
controller.button_a.on_down = on_a_down

# 摇杆
def on_abs_move(obj):
    print(f'{obj.name}: x:{obj.x}, y:{obj.y}, z:{obj.z}')

controller.hat.on_move = on_abs_move
controller.axis_l.on_move = on_abs_move


controller.start()
while 1:
    time.sleep(1)

```


完整用法请查看: [examples](examples) 

Compatibility
-------------
只在树莓派系统测试，其他系统兼容未知. 

Licence
-------
We use a shared copyright model that enables all contributors to maintain the
copyright on their contributions.

See the [LICENSE](LICENSE) file in this repository for details.

Authors
-------

`xbox360gamepad` was written by `huzhiwu <job@huzhiwu.com>`_.
