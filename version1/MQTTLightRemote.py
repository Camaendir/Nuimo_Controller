from matrices import *
from DeviceManager import Remote, Device, DeviceManager, Direction
from time import sleep


class LightRemote(Remote):
    def __init__(self, indication_number, topic_prefix, device_manager: DeviceManager,
                 base_matrix=lightbulb_matrix, enable_multiple_press=False):
        super().__init__(get_indicates_matrix(base_matrix, indication_number), enable_multiple_press=enable_multiple_press)
        self.on_topic = topic_prefix + "/on"
        self.topic_prefix = topic_prefix
        self.on = False
        self.mqtt = device_manager.get_mqtt_manager()
        self.mqtt.register_subscription(self.on_topic, self.mqtt_on_message)

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

    def on_press(self, device: Device):
        self.on = not self.on
        self.mqtt.publish(self.on_topic, "1" if self.on else "0")
        self.light_animation(device, reverse=not self.on)

    def mqtt_on_message(self, payload):
        self.on = (payload.decode() == "1")


class BrightnessLightRemote(LightRemote):
    def __init__(self, indication_number, topic_prefix, device_manager: DeviceManager, base_matrix=lightbulb_matrix, enable_multiple_press=False):
        super().__init__(indication_number, topic_prefix, device_manager, base_matrix, enable_multiple_press=enable_multiple_press)
        self.value = 0
        self.brightness_topic = topic_prefix + "/brightness"
        self.mqtt.register_subscription(self.brightness_topic, self.mqtt_brightness_message)

    def mqtt_brightness_message(self, payload):
        self.value = int(payload.decode())

    def on_rotate(self, value, device: Device):
        self.value += self.slow_acceleration_curve(value)
        self.value = min(100, self.value)
        self.value = max(0, self.value)
        device.send_matrix(get_matrix_from_number(int(self.value)), interval=1, fading=True)
        self.mqtt.publish(self.brightness_topic + "/debounce", int(self.value))


class LumibaerRemote(BrightnessLightRemote):

    def __init__(self, indication_number, topic_prefix, device_manager: DeviceManager, base_matrix=lightbulb_matrix):
        super().__init__(indication_number, topic_prefix, device_manager, base_matrix)
        self.mqtt = device_manager.get_mqtt_manager()
        self.colors = [wave_matrix, fire_matrix, ying_matrix, leaf_matrix]
        self.color_status = 0

    def on_swipe(self, direction: Direction, device: Device):
        if direction == Direction.TOP:
            self.mqtt.publish(self.topic_prefix + "/status", 1)
            device.send_matrix(star_matrix, interval=3)
        elif direction == Direction.BOTTOM:
            self.mqtt.publish(self.topic_prefix + "/status", 0)
            device.send_matrix(lightbulb_matrix, interval=3)
        elif direction == Direction.RIGHT:
            self.color_status = (self.color_status + 1) % len(self.colors)
            self.mqtt.publish(self.topic_prefix + "/color/set", self.color_status)
            device.send_matrix(self.colors[self.color_status])
        elif direction == Direction.LEFT:
            self.color_status = (self.color_status - 1) % len(self.colors)
            self.mqtt.publish(self.topic_prefix + "/color/set", self.color_status)
            device.send_matrix(self.colors[self.color_status])


class SignRemote(BrightnessLightRemote):

    def __init__(self, indication_number, topic_prefix, device_manager: DeviceManager, base_matrix=lightbulb_matrix):
        super().__init__(indication_number, topic_prefix, device_manager, base_matrix)
        self.mqtt = device_manager.get_mqtt_manager()

    def on_swipe(self, direction: Direction, device: Device):
        if direction == direction.TOP:
            self.mqtt.publish(self.topic_prefix + "/status", 1)
            device.send_matrix(snake_matrix, interval=3)
        elif direction == direction.BOTTOM:
            self.mqtt.publish(self.topic_prefix + "/status", 0)
            device.send_matrix(lightbulb_matrix, interval=3)
        else:
            super().on_swipe(direction, device)

