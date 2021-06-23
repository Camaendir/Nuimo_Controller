from enum import Enum
import paho.mqtt.client as mqtt
from time import sleep
import nuimo

class Direction(Enum):
    LEFT = 0
    RIGHT = 1
    TOP = 2
    BOTTOM = 3

class SubController:
    def __init__(self, light_up_matrix, controller, manager):
        self.active = False
        self.controller = controller
        self.manager = manager
        self.manager.register(self)
        self.light_up_matrix = light_up_matrix
    
    def activate(self):
        self.active = True
        self.send_matrix(self.light_up_matrix, interval=5)
    
    def deactivate(self):
        self.active = False
    
    def send_matrix(self, matrix, interval=2.0, fading=True):
        self.controller.display_matrix(matrix, interval=interval, fading=fading)

    def on_rotate(self, value):
        pass

    def on_press(self):
        pass

    def on_release(self):
        pass
    
    def on_swipe(self, direction: Direction):
        pass

    def on_touch(self, direction: Direction):
        pass

    def on_long_touch(self, direction: Direction):
        pass

class MQTTClientManager(nuimo.ControllerListener):

    def __init__(self, controller):
        self.controller = controller
        self.client = mqtt.Client("Nuimo")
        self.subscriptions = []
        self.client.on_message = self.on_message
        self.client.on_disconnect = self.reconnect_client
        self.client.on_connect = self.on_connect
        self.client.connect("localhost")
        self.client.loop_start()

        self.active = None
        self.active_index = -1
        self.submodules = []
    
    def change_active(self, increase_by=1):
        if self.active:
            self.active.deactivate()
            if isinstance(self.active, MQTTSubController):
                for t in self.submodules[self.active_index][1]:
                    self.client.unsubscribe(t)
            self.active_index += increase_by
            self.active_index %= len(self.submodules)
            self.active = self.submodules[self.active_index][0]
            self.active.activate()
            if isinstance(self.active, MQTTSubController):
                for t in self.submodules[self.active_index][1]:
                    self.client.subscribe(t)
        else:
            if self.submodules != []:
                self.active_index = 0
                self.active = self.submodules[0][0]
                self.active.activate()
                if isinstance(self.active, MQTTSubController):
                    for t in self.submodules[0][1]:
                        self.client.subscribe(t)

    def register(self, _instance: SubController):
        if isinstance(_instance, MQTTSubController):
            topics = _instance.get_topics()
            self.subscriptions.extend(topics)
            self.submodules.append((_instance, topics))
        else:
            self.submodules.append((_instance, None))
        if not self.active:
            self.active_index = 0
            self.active = self.submodules[0][0]
            for t in self.submodules[0][1]:
                self.client.subscribe(t)

    def on_message(self, client, userdata, message):
        if isinstance(self.active, MQTTSubController):
            if message.topic in self.submodules[self.active_index][1]:
                self.active.on_message(message.topic, message.payload)

    def reconnect_client(self, client, userdata, rc):
        client.connect("localhost")

    def received_gesture_event(self, event):
        val = event.gesture.value
        if not isinstance(val, int):
            val = val[0]
        if val == 1: # button press
            self.active.on_press()
        elif val == 2: # release
            self.active.on_release()
        elif val >= 3 and val <= 6: # SWIPE
            direction = Direction(val - 3)
            self.active.on_swipe(direction)
        elif val >=8 and val <= 11: # TOUCH
            direction = Direction(val - 8)
            self.active.on_touch(direction)
        elif val >= 12 and val <= 15: # LONGTOUCH
            direction = Direction(val - 12)
            if direction == Direction.LEFT:
                self.change_active(-1)
            elif direction == Direction.RIGHT:
                self.change_active(1)
            else:
                self.active.on_longtouch(direction)
        elif val == 16: # ROTATION
            self.active.on_rotate(event.value)

    def on_connect(self, client, userdata, flags, rc):
        for s in self.subscriptions:
            client.subscribe(s[0])
    
    def publish(self, topic, payload, retained=False):
        self.client.publish(topic, payload)
    
    def disconnect_succeeded(self):
        print("disconnected")
        self.controller.connect()

    def connect_failed(self, error):
        print("Connected!")

class MQTTSubController(SubController):
    def __init__(self,light_up_matrix, controller, topics, manager):
        self.topics = topics
        super().__init__(light_up_matrix, controller, manager)
    
    def get_topics(self):
        return self.topics
    
    def on_message(self, topic, payload):
        pass

    def publish(self, topic, message):
        self.manager.publish(topic, message)
