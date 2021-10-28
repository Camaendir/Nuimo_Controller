from collections import Iterable

import nuimo
import threading
import paho.mqtt.client as mqtt
from enum import Enum
from threading import Timer


class Direction(Enum):
    LEFT = 0
    RIGHT = 1
    TOP = 2
    BOTTOM = 3


# manager -> multiple controller (Device) -> each one sub-controller -> passes onto Remote (not controller specific)

"""
manager = Manager(bluetooth_adapter)
device1 = Device(manager, mac1)
device2 = Device(manager, mac2)


spotify = SpotifyRemote(parameter)
lumibaer = LumibaerRemote(parameter)
sign = SignRemote(parameter)

weather = WeatherRemote(parameter)

device1.register([spotify, lumibaer, sign])
device2.register([spotify, lumibaer, sign, weather])

manager.run()
"""


class SubController(nuimo.ControllerListener):

    def __init__(self, device):
        self.device = device
        self.active: Remote = None
        self.active_index = -1
        self.remotes = []
        self.press_delay = 1
        self.already_pressed = 0
        self.already_released = False

    def change_active(self, increase_by=1):
        if self.active:
            self.active.deactivate(self.device)
            self.active_index += increase_by
            self.active_index %= len(self.remotes)
            self.active = self.remotes[self.active_index]
            self.active.activate(self.device)
            self.active.indicate(self.device)
        else:
            if self.remotes:
                self.active_index = 0
                self.active = self.remotes[0]
                self.active.activate(self.device)
                self.active.indicate(self.device)

    def register_remote(self, remote):
        self.remotes.append(remote)
        if not self.active:
            self.active_index = 0
            self.active = self.remotes[0]
            self.active.activate(self.device)
            self.active.indicate(self.device)

    def check_press(self, press_number):
        if self.already_pressed == press_number:
            if self.already_pressed == 1:
                self.already_pressed = 0
                self.active.on_press(self.device)
                if self.already_released:
                    self.active.on_release(self.device)
            else:
                self.active.on_multiple_press(self.already_pressed, self.device)
                self.already_pressed = 0

    def received_gesture_event(self, event):
        if not self.active:
            return
        val = event.gesture.value
        if not isinstance(val, int):
            val = val[0]

        if val == 1:  # button press
            if self.active.enable_multiple_press:
                self.already_pressed += 1
                Timer(self.press_delay, self.check_press, [self.already_pressed]).start()
            else:
                self.active.on_press(self.device)

        elif val == 2:  # release
            if self.active.enable_multiple_press:
                if self.already_pressed == 0:
                    self.active.on_release(self.device)
                else:
                    self.already_released = True
            else:
                self.active.on_release(self.device)

        elif 3 <= val <= 6:  # SWIPE
            direction = Direction(val - 3)
            if direction == Direction.LEFT:  # Change active Remote
                self.change_active(-1)
            elif direction == Direction.RIGHT:
                self.change_active(1)
            else:
                self.active.on_swipe(direction, self.device)
        elif 8 <= val <= 11:  # TOUCH
            direction = Direction(val - 8)
            if direction == Direction.BOTTOM:  # Indicate active Remote
                self.active.indicate(self.device)
            else:
                self.active.on_touch(direction, self.device)

        elif 12 <= val <= 15:  # LONG TOUCH
            direction = Direction(val - 12)
            self.active.on_long_touch(direction, self.device)

        elif val == 16:  # ROTATION
            self.active.on_rotate(event.value, self.device)

    def disconnect_succeeded(self):
        print("Device " + self.device.name + " with mac " + self.device.mac + " disconnected!\nTrying to reconnect...")
        self.device.connect()

    def started_connecting(self):
        print("Trying to connect to " + self.device.name)

    def connect_succeeded(self):
        print("Connecting succeeded with " + self.device.name)

    def connect_failed(self, error):
        if str(error) == "Nuimo GATT service missing":
            print("Device " + self.device.name + " connected")
            if self.active:
                self.active.indicate(self.device)
        else:
            print("Connecting to " + self.device.name + " failed:", error)

    def started_disconnecting(self):
        print("Started disconnecting from " + self.device.name)


class Device:
    def __init__(self, device_manager, mac, name):
        self.controller = nuimo.Controller(mac_address=mac, manager=device_manager.manager)
        self.subController = SubController(self)
        self.controller.listener = self.subController
        self.name = name
        self.mac = mac
        self.device_manager = device_manager
        self.device_manager.register_device(self)

    def _register(self, remote):
        self.subController.register_remote(remote)

    def register_remotes(self, remotes):
        if isinstance(remotes, Iterable):
            for r in remotes:
                self._register(r)
        else:
            self._register(remotes)

    def send_matrix(self, matrix, interval=3, fading=True):
        self.controller.display_matrix(nuimo.LedMatrix(matrix), interval=interval, fading=fading)

    def connect(self, _continue=True):
        self.controller.connect()

class DeviceManager:

    def __init__(self, adapter_name="hci0"):
        self.manager = nuimo.ControllerManager(adapter_name=adapter_name)
        self.devices = []
        self.mqtt_manager = None

    def get_mqtt_manager(self):
        if not self.mqtt_manager:
            self.mqtt_manager = MQTTManager()
        return self.mqtt_manager

    def register_device(self, device: Device):
        self.devices.append(device)

    def run(self):
        for device in self.devices:
            device.connect()
        x = threading.Thread(target=self.manager.run)
        x.start()


class Remote:
    def __init__(self, light_up_matrix, enable_multiple_press=False):
        self.active = False
        self.light_up_matrix = light_up_matrix
        self.enable_multiple_press = enable_multiple_press

    def activate(self, device: Device):
        self.active = True

    def indicate(self, device: Device):
        device.send_matrix(self.light_up_matrix, interval=4)

    def deactivate(self, device: Device):
        self.active = False

    def on_rotate(self, value, device: Device):
        pass

    def on_multiple_press(self, value, device: Device):
        pass

    def on_press(self, device: Device):
        pass

    def on_release(self, device: Device):
        pass

    def on_swipe(self, direction: Direction, device: Device):
        pass

    def on_touch(self, direction: Direction, device: Device):
        pass

    def on_long_touch(self, direction: Direction, device: Device):
        pass

    def slow_acceleration_curve(self, value):
        sign = -1 if value < 0 else 1
        value = abs(value)
        value = pow(value, 1.6) * 0.00015
        return sign * value

    def fast_acceleration_curve(self, value):
        sign = -1 if value < 0 else 1
        value = abs(value)
        value = pow(value, 1.7) * 0.0002
        return sign * value


class MQTTManager:
    def __init__(self, host="localhost", port=1883, client_name="Nuimo_Manager"):
        self.host = host
        self.port = port
        self.mqtt_client = mqtt.Client(client_name)
        self.mqtt_client.on_message = self.on_message
        self.mqtt_client.on_disconnect = self.reconnect_client
        self.mqtt_client.on_connect = self.on_connect
        self.mqtt_client.connect(host, port)
        self.mqtt_client.loop_start()
        self.subscriptions = {}

    def register_subscription(self, topic, function):
        if topic in self.subscriptions.keys():
            self.subscriptions[topic].append(function)
        else:
            self.subscriptions[topic] = [function]
            self.mqtt_client.subscribe(topic)

    def on_message(self, client, userdata, message):
        topic = message.topic
        payload = message.payload
        if topic in self.subscriptions.keys():
            for f in self.subscriptions[topic]:
                f(payload)

    def on_connect(self, client, userdata, flags, rc):
        for topic in self.subscriptions.keys():
            self.mqtt_client.subscribe(topic)

    def reconnect_client(self, client, userdata, rc):
        self.mqtt_client.connect(self.host, self.port)

    def publish(self, topic, payload, retain=True):
        self.mqtt_client.publish(topic, payload, retain=retain)
