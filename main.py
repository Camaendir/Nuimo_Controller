import nuimo
import threading
import paho.mqtt.client as mqtt
import paho.mqtt.subscribe as subscribe
import math
from time import sleep


class MQTTListener(nuimo.ControllerListener):

    def __init__(self):
        self.client = mqtt.Client("Nuimo")
        self.client.connect("localhost")
        self.buffer = []
        self.running = False
        self.thread = threading.Thread(target=self.send_average)
        self.client.on_message = MQTTListener.on_message
        self.client.subscribe("nuimo/spotify/volume/get")

    def publish_volume_set(self, volume):
        self.client.publish("spotify/volume/set", str(volume))

    def publish_volume_increase(self, volume):
        self.client.publish("spotify/volume/increase", str(volume))

    def send_play_pause(self):
        self.client.publish("spotify/play_state/set", "")

    def flatten(self, volume):
        self.buffer += 1
        if self.buffer == 10:
            self.publish_volume_set(volume)
            self.buffer = 0
            self.update_matrix(volume)

    @staticmethod
    def update_matrix(vol):
        rank = math.floor(81 / 100 * vol)
        matrix = nuimo.LedMatrix(" " * (81 - rank) + "*" * rank)
        controller.display_matrix(matrix, interval=30, fading=True)

    @staticmethod
    def on_message(client, userdata, message):
        if message.topic == "nuimo/spotify/volume/get":
            MQTTListener.update_matrix(int(message.payload))

    def send_average(self):
        print("send in 1 sec")
        sleep(1.0)
        print("send now")
        val_sum = sum(self.buffer)
        self.buffer = []
        self.publish_volume_increase(val_sum)
        print("send via mqtt")
        self.thread = threading.Thread(target=self.send_average)
        self.running = False
        print("reset variables")

    def received_gesture_event(self, event):
        if (event.gesture == nuimo.Gesture.ROTATION):
            self.buffer.append(event.value)
            if not self.running:
                self.running = True
                self.thread.start()
        elif event.gesture == nuimo.Gesture.BUTTON_PRESS:
            self.send_play_pause()

    def started_connecting(self):
        print("started connecting")

    def connect_succeeded(self):
        print("connect sucessfull")

    def connect_failed(self, error):
        print("connect failed", error)

    def started_disconnecting(self):
        print("started disconnecting")

    def disconnect_succeeded(self):
        print("disconnect succeded")


manager = nuimo.ControllerManager(adapter_name='hci0')
print("Using Mac: dc:1c:77:d0:9a:d9")
controller = nuimo.Controller(mac_address='dc:1c:77:d0:9a:d9', manager=manager)
controller.listener = MQTTListener()
controller.connect()
x = threading.Thread(target=manager.run)
x.start()
