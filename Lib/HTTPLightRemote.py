from matrices import *
from .DeviceManager import Remote, Device, Direction
from time import sleep, time
import requests


class LightRemote(Remote):
    def __init__(self, indication_number, http_ip, base_matrix=lightbulb_matrix, enable_multiple_press=False):
        super().__init__(get_indicates_matrix(base_matrix, indication_number),
                         enable_multiple_press=enable_multiple_press)
        self.on = self.get_http("/on").lower() == "true"
        self.http_ip = http_ip
        self.data_timer_on = time()

    def light_animation(self, device: Device, reverse=False):
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

    def send_http(self, path, message):
        requests.post("http://" + self.http_ip + path, data=message)

    def get_http(self, path):
        return requests.get("http://" + self.http_ip + path).text

    def on_press(self, device: Device):
        if time() - self.data_timer_on > 5:
            self.on = self.get_http("/on") == "true"
        self.on = not self.on
        self.send_http("/on", "true")
        self.light_animation(device, reverse=not self.on)
        self.data_timer_on = time()


class BrightnessLightRemote(LightRemote):
    def __init__(self, indication_number, http_ip, base_matrix=lightbulb_matrix, enable_multiple_press=False):
        super().__init__(indication_number, http_ip, base_matrix, enable_multiple_press=enable_multiple_press)
        self.value = float(int(self.get_http("/bri")))
        self.data_timer_bri = time()

    def on_rotate(self, value, device: Device):
        if time() - self.data_timer_bri > 5:
            self.value = int(self.get_http("/bri"))
        self.value += self.slow_acceleration_curve(value)
        self.value = min(100, self.value)
        self.value = max(0, self.value)
        device.send_matrix(get_matrix_from_number(int(self.value)), interval=1, fading=True)
        self.send_http("/bri", str(int(self.value)))


class LumibaerRemote(BrightnessLightRemote):

    def __init__(self, indication_number, http_ip, base_matrix=lightbulb_matrix):
        super().__init__(indication_number, http_ip, base_matrix)
        self.colors_matrices = [wave_matrix, fire_matrix, ying_matrix, leaf_matrix]
        self.color_values = [(231, 100), (0, 100), (27, 95), (110, 96)]
        self.color_status = 0

    def update_colors(self, matrices, values):
        assert len(matrices) == len(values)
        self.color_values = values
        self.colors_matrices = matrices

    def change_animation(self, device: Device):
        self.send_http("/sat", str(self.color_values[self.color_status][1]))
        self.send_http("/hue", str(self.color_values[self.color_status][0]))
        device.send_matrix(self.colors_matrices[self.color_status])

    def on_swipe(self, direction: Direction, device: Device):
        if direction == Direction.TOP:
            self.send_http("/ani", str(1))
            device.send_matrix(star_matrix, interval=3)
        elif direction == Direction.BOTTOM:
            self.send_http("/ani", str(0))
            device.send_matrix(lightbulb_matrix, interval=3)
        elif direction == Direction.RIGHT:
            self.color_status = (self.color_status + 1) % len(self.color_values)
            self.change_animation(device)
        elif direction == Direction.LEFT:
            self.color_status = (self.color_status - 1) % len(self.color_values)
            self.change_animation(device)
