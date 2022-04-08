from matrices import *
from .DeviceManager import Remote, Device, DeviceManager, Direction
from time import sleep, time
import json
import threading


class LightRemote(Remote):
    def __init__(self, indication_number, topic_prefix, device_manager: DeviceManager,
                 base_matrix=lightbulb_matrix, enable_multiple_press=False):
        super().__init__(get_indicates_matrix(base_matrix, indication_number),
                         enable_multiple_press=enable_multiple_press)
        self.on_topic = topic_prefix + "/on"
        self.topic_prefix = topic_prefix
        self.on = True
        self.mqtt = device_manager.get_mqtt_manager()
        self.mqtt.register_subscription(self.on_topic, self.mqtt_on_message)

    def light_animation(self, device: Device, reverse=False):
        if not reverse:
            device.send_matrix(self, light_matrix_3, interval=1.1)
            sleep(1)
            device.send_matrix(self, light_matrix_2, interval=1.1)
            sleep(1)
            device.send_matrix(self, light_matrix, interval=1.1)
        else:
            device.send_matrix(self, light_matrix, interval=1.1)
            sleep(1)
            device.send_matrix(self, light_matrix_2, interval=1.1)
            sleep(1)
            device.send_matrix(self, light_matrix_3, interval=1.1)

    def on_press(self, device: Device):
        self.on = not self.on
        self.mqtt.publish(self.on_topic, "1" if self.on else "0")
        self.light_animation(device, reverse=not self.on)

    def mqtt_on_message(self, payload):
        self.on = (payload.decode() == "1")


class JSONLightRemote(Remote):
    def __init__(self, indication_number, pub_topic, sub_topic, device_manager, json_key="state",
                 json_values=("OFF", "ON"), base_matrix=lightbulb_matrix, enable_multiple_press=False):
        super().__init__(get_indicates_matrix(base_matrix, indication_number),
                         enable_multiple_press=enable_multiple_press)
        self.pub_topic = pub_topic
        self.on = True
        self.mqtt = device_manager.get_mqtt_manager()
        self.mqtt.register_subscription(sub_topic, self.mqtt_on_message)
        self.json_key = json_key
        self.json_values = json_values

    def light_animation(self, device: Device, reverse=False):
        if not reverse:
            device.send_matrix(self, light_matrix_3, interval=1.1)
            sleep(1)
            device.send_matrix(self, light_matrix_2, interval=1.1)
            sleep(1)
            device.send_matrix(self, light_matrix, interval=1.1)
        else:
            device.send_matrix(self, light_matrix, interval=1.1)
            sleep(1)
            device.send_matrix(self, light_matrix_2, interval=1.1)
            sleep(1)
            device.send_matrix(self, light_matrix_3, interval=1.1)

    def on_press(self, device: Device):
        self.on = not self.on
        self.mqtt.publish(self.pub_topic, json.dumps({self.json_key: self.json_values[int(self.on)]}))
        threading.Thread(target=self.light_animation, args=(device, not self.on)).start()

    def mqtt_on_message(self, paylaod):
        data = json.loads(paylaod.decode())
        if self.json_key in data:
            self.on = data[self.json_key] == self.json_values[1]


class BrightnessLightRemote(LightRemote):
    def __init__(self, indication_number, topic_prefix, device_manager: DeviceManager, base_matrix=lightbulb_matrix,
                 enable_multiple_press=False):
        super().__init__(indication_number, topic_prefix, device_manager, base_matrix,
                         enable_multiple_press=enable_multiple_press)
        self.value = 0
        self.brightness_topic = topic_prefix + "/brightness"
        self.mqtt.register_subscription(self.brightness_topic, self.mqtt_brightness_message)

    def mqtt_brightness_message(self, payload):
        self.value = int(payload.decode())

    def on_rotate(self, value, device: Device):
        self.value += self.slow_acceleration_curve(value)
        self.value = min(100, self.value)
        self.value = max(0, self.value)
        device.send_matrix(self, get_matrix_from_number(int(self.value)), interval=1, fading=True)
        self.mqtt.publish(self.brightness_topic + "/debounce", int(self.value))


class LumibaerRemote(Remote):

    def __init__(self, device_manager: DeviceManager, base_matrix=lightbulb_matrix):
        super().__init__(base_matrix)
        self.mqtt = device_manager.get_mqtt_manager()

        self.status_topic = "/Lumibaer/status"
        self.color_topic = "/Lumibaer/parameter"
        self.brightness_topic = "/Lumibaer/brightness"

        self.on = True

        self.brightness = 50

        self.color_matrices = [wave_matrix, fire_matrix, ying_matrix, leaf_matrix]
        self.colors = [(0, 0, 255), (255, 0, 0), (250, 175, 0), (0, 255, 0)]
        self.color_index = 0
        self.color_status = 5

        self.status_matrices = [stop_matrix, step_matrix, rainbow_matrix, rocket_matrix, matrix_matrix]
        self.status = 0

        self.rotate_status = 0
        self.rotate_timer = 0
        self.rotate_timeout = 3
        self.rotate_value = 0
        self.rotate_change_selection_value = 10

    def send_status(self, status):
        self.mqtt.publish(self.status_topic, str(status))

    def send_brightness(self, brightness):
        self.mqtt.publish(self.brightness_topic, str(brightness))

    def light_animation(self, device: Device, reverse=False):
        if not reverse:
            device.send_matrix(self, light_matrix_3, interval=0.5)
            sleep(0.5)
            device.send_matrix(self, light_matrix_2, interval=0.5)
            sleep(0.5)
            device.send_matrix(self, light_matrix, interval=0.5)
        else:
            device.send_matrix(self, light_matrix, interval=0.5)
            sleep(0.5)
            device.send_matrix(self, light_matrix_2, interval=0.5)
            sleep(0.5)
            device.send_matrix(self, light_matrix_3, interval=0.5)

    def on_press(self, device: Device):
        self.check_reset()
        self.on = not self.on
        self.send_status(self.status if self.on else 0)
        self.light_animation(device, reverse=not self.on)

    def check_reset(self):
        if time() - self.rotate_timer > self.rotate_timeout:
            self.rotate_status = 0
            self.rotate_value = 0

    def send_color(self, color_index):
        self.mqtt.publish(self.color_topic, "/".join(map(str, self.colors[color_index])))

    def on_rotate(self, value, device: Device):
        self.check_reset()
        value = self.slow_acceleration_curve(value)
        if self.rotate_status == 0:
            self.brightness = max(min(value + self.brightness, 100), 0)
            self.send_brightness(self.brightness)
            device.send_matrix(self, get_matrix_from_number(int(self.brightness)), interval=1, fading=True)
        elif self.rotate_status == 1:
            self.rotate_timer = time()
            self.rotate_value += value
            if self.rotate_value > self.rotate_change_selection_value:
                self.status += 1
                self.status %= len(self.status_matrices)
                self.rotate_value = 0
                device.send_matrix(self, self.status_matrices[self.status])
                if self.on:
                    self.send_status(self.status)
            elif self.rotate_value < (-1 * self.rotate_change_selection_value):
                self.status -= 1
                self.rotate_value = 0
                self.status %= len(self.status_matrices)
                device.send_matrix(self, self.status_matrices[self.status])
                if self.on:
                    self.send_status(self.status)
        elif self.rotate_status == 2:
            self.rotate_timer = time()
            self.rotate_value += value
            if self.rotate_value > self.rotate_change_selection_value:
                self.color_index += 1
                self.color_index %= len(self.color_matrices)
                self.rotate_value = 0
                device.send_matrix(self, self.color_index)
                if self.on:
                    self.send_color(self.colors[self.color_index])
            elif self.rotate_value < (-1 * self.rotate_change_selection_value):
                self.color_index -= 1
                self.color_index %= len(self.color_matrices)
                self.rotate_value = 0
                device.send_matrix(self, self.color_matrices[self.color_index])
                if self.on:
                    self.send_color(self.color_index)

    def on_swipe(self, direction: Direction, device: Device):
        if direction == Direction.TOP:
            if self.rotate_status == 2:
                self.rotate_status = 0
                device.send_matrix(self, get_matrix_from_number(int(self.brightness)))
            else:
                device.send_matrix(self, arrow_matrix)
                self.rotate_status = 1
                self.rotate_timer = time()
        elif direction == Direction.BOTTOM:
            if self.rotate_status == 1:
                self.rotate_status = 0
                device.send_matrix(self, get_matrix_from_number(int(self.brightness)))
            else:
                device.send_matrix(self, star_matrix)
                self.rotate_status = 2
                self.rotate_timer = time()


class SignRemote(BrightnessLightRemote):

    def __init__(self, indication_number, topic_prefix, device_manager: DeviceManager, base_matrix=lightbulb_matrix):
        super().__init__(indication_number, topic_prefix, device_manager, base_matrix)
        self.mqtt = device_manager.get_mqtt_manager()

    def on_swipe(self, direction: Direction, device: Device):
        if direction == direction.TOP:
            self.mqtt.publish(self.topic_prefix + "/status", 1)
            device.send_matrix(self, snake_matrix, interval=3)
        elif direction == direction.BOTTOM:
            self.mqtt.publish(self.topic_prefix + "/status", 0)
            device.send_matrix(self, lightbulb_matrix, interval=3)
        else:
            super().on_swipe(direction, device)
