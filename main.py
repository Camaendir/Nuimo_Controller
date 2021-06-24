import nuimo
import threading
import math
from time import sleep
from matrices import *
from Controller import *
from enum import Enum





class SpotifyController(MQTTSubController):
    def __init__(self, light_up_matrix, controller, manager, topics=("nuimo/spotify/status/get", "nuimo/spotify/volume/get")):
        super().__init__(light_up_matrix, controller, topics, manager)
        self.value = 0
        self.publish("spotify/volume/need", "")
    
    def on_message(self, topic, payload):
        if topic == "nuimo/spotify/status/get":
            self.update_matrix_status(payload == b"true")
        elif topic == "nuimo/spotify/volume/get":
            self.value = int(payload)

    def update_matrix_status(self, status):
        if status:
            self.send_matrix(play_matrix, interval=5, fading=True)
        else:
            self.send_matrix(pause_matrix, interval=5, fading=True)

    def on_rotate(self, value):
        sign = -1 if value < 0 else 1
        value = abs(value)
        value = pow(value, 1.6) * 0.00015
        self.value += (sign * value)
        self.value = min(100, self.value)
        self.value = max(0, self.value)
        self.send_matrix(get_matrix_from_number(int(self.value)), interval=1, fading=True)
        self.publish("spotify/volume/set", int(self.value))
    
    def on_press(self):
        self.publish("spotify/play_state/set", "")
    
    def on_swipe(self, direction):
        if direction == direction.LEFT:
            self.publish("spotify/song/previous", "")
            self.send_matrix(last_matrix)
        elif direction == direction.RIGHT:
            self.publish("spotify/song/next", "")
            self.send_matrix(next_matrix)
        elif direction == direction.TOP:
            self.publish("hall/rfid/found", "true")
            self.send_matrix(loudspeaker_matrix)
        elif direction == direction.BOTTOM:
            self.publish("spotify/play/endomorphismus", "")
            self.send_matrix(heart_matrix)


class LightController(MQTTSubController):
    def __init__(self, indication_number, topic_prefix, controller, manager, additional_topic=None):
        self.on_topic = topic_prefix + "/on"
        self.topic_prefix = topic_prefix
        super().__init__(get_indicates_matrix(lightbulb_symbol, indication_number), controller, [self.on_topic] + additional_topic, manager)
        self.on = False

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
        self.publish(self.on_topic, "0" if self.on else "1")
        self.light_animation(reverse=not self.on)

    def on_message(self, topic, payload):
        if topic == self.on_topic:
            self.on = (payload.decode() == "1")


class BrightnessLightController(LightController):
    def __init__(self, indication_number, topic_prefix, controller, manager, additional_topics=None):
        self.brightness_topic = topic_prefix + "/brightness"
        super().__init__(indication_number, topic_prefix, controller, manager, [self.brightness_topic])
        self.value = 0

    def on_message(self, topic, payload):
        if topic == self.brightness_topic:
            self.value = int(payload.decode())
        else:
            super().on_message(topic, payload)

    def on_rotate(self, value):
        self.value += value / 300
        self.value = min(100, self.value)
        self.value = max(0, self.value)
        self.send_matrix(get_matrix_from_number(int(self.value)), interval=1, fading=True)
        self.publish(self.brightness_topic + "/debounce", int(self.value))


mac_use = 0
macs = ("dc:1c:77:d0:9a:d9", "CB:DB:5D:3E:34:6E")
manager = nuimo.ControllerManager(adapter_name='hci0')
print("Using Mac: ", macs[mac_use])
controller = nuimo.Controller(mac_address=macs[mac_use], manager=manager)
man = MQTTClientManager(controller)
controller.listener = man

SpotifyController(music_matrix, controller, man)
BrightnessLightController(2, "hall/sign", controller, man)
BrightnessLightController(1, "room/lumibaer", controller, man)

print("connecting ...")
controller.connect()
x = threading.Thread(target=manager.run)
x.start()
