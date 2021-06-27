from DeviceManager import Device, Remote
from matrices import *
from time import sleep
from env import phillips_hue_bridge_ip
from phue import Bridge


class HueRemote(Remote):

    def __init__(self, light_indicator, device_group_name, is_group=True, has_brightness=True,
                 base_matrix=lightbulb_matrix):
        super().__init__(get_indicates_matrix(base_matrix, light_indicator), )
        self.has_brightness = has_brightness
        self.is_group = is_group
        self.b = Bridge(phillips_hue_bridge_ip)
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

    def on_rotate(self, value, device: Device):
        if not self.has_brightness:
            return
        self.value += value / 300
        self.value = min(100, self.value)
        self.value = max(0, self.value)
        device.send_matrix(get_matrix_from_number(int(self.value)), interval=1, fading=True)
        if self.is_group:
            self.b.set_group(self.name, "bri", int(self.value * 2.54))
        else:
            self.b.set_light(self.name, "bri", int(self.value * 2.54))

    def light_animation(self, device: Device, reverse=False, ):
        if not reverse:
            device.send_matrix(light_matrix_3, interval=1.1)
            sleep(1)
            device.send_matrix(light_matrix_2, interval=1.1)
            sleep(1)
            device.send_matrix(light_matrix, interval=1.1)
        else:
            device.send_matrix(light_matrix, interval=1.1)
            sleep(1)
            device.send_matrix(light_matrix_2, interval=1.1)
            sleep(1)
            device.send_matrix(light_matrix_3, interval=1.1)

    def on_press(self, device: Device):
        self.on = not self.on
        if self.is_group:
            self.b.set_group(self.name, "on", self.on)
        else:
            self.b.set_light(self.name, "on", self.on)
        self.light_animation(device, reverse=not self.on)
