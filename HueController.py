from Controller import SubController
from matrices import *
from time import sleep


class HueController(SubController):

    def __init__(self, light_indicator, bridge_id, device_group_name, controller, manager, is_group=True,
                 has_brightness=True):
        super().__init__(get_indicates_matrix(light_matrix, light_indicator), controller, manager, False)
        from phue import Bridge
        self.has_brightness = has_brightness
        self.is_group = is_group
        self.b = Bridge(bridge_id)
        self.b.connect()
        if self.is_group:
            self.on = self.b.get_group(device_group_name, "on")
            if self.has_brightness:
                self.value = self.b.get_group(device_group_name, "bri")
        else:
            self.on = self.b.get_light(device_group_name, "on")
            if self.has_brightness:
                self.value = self.b.get_light(device_group_name, "bri")
        self.name = device_group_name

    def on_rotate(self, value):
        if not self.has_brightness:
            return
        self.value += value / 300
        self.value = min(100, self.value)
        self.value = max(0, self.value)
        self.send_matrix(get_matrix_from_number(int(self.value)), interval=1, fading=True)
        if self.is_group:
            self.b.set_group(self.name, "bri", int(self.value * 2.54))
        else:
            self.b.set_light(self.name, "bri", int(self.value * 2.54))

    def light_animation(self, reverse=False):
        if not reverse:
            self.send_matrix(light_matrix_3, interval=1.1)
            sleep(1)
            self.send_matrix(light_matrix_2, interval=1.1)
            sleep(1)
            self.send_matrix(light_matrix, interval=1.1)
        else:
            self.send_matrix(light_matrix, interval=1.1)
            sleep(1)
            self.send_matrix(light_matrix_2, interval=1.1)
            sleep(1)
            self.send_matrix(light_matrix_3, interval=1.1)

    def on_press(self):
        self.on = not self.on
        if self.is_group:
            self.b.set_group(self.name, "on", self.on)
        else:
            self.b.set_light(self.name, "on", self.on)
        self.light_animation(reverse=not self.on)
