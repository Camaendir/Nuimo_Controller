import nuimo
import threading
import math
from time import sleep
from matrices import *
from Controller import *
from enum import Enum





class SpotifyController(MQTTSubController):
    def __init__(self, controller, manager, topics=["nuimo/spotify/status/get", "nuimo/spotify/volume/get"]):
        super().__init__(controller, topics, manager)
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
        self.value += value / 300
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



manager = nuimo.ControllerManager(adapter_name='hci0')
print("Using Mac: dc:1c:77:d0:9a:d9")
controller = nuimo.Controller(mac_address='dc:1c:77:d0:9a:d9', manager=manager)
man = MQTTClientManager()
controller.listener = man

SpotifyController(controller, man)

print("connecting ...")
controller.connect()
x = threading.Thread(target=manager.run)
x.start()
