WITHMQTT = False

from enum import Enum
from threading import Timer
import nuimo


if WITHMQTT:
    import paho.mqtt.client as mqtt


class Direction(Enum):
    LEFT = 0
    RIGHT = 1
    TOP = 2
    BOTTOM = 3

class SubController:
    def __init__(self, light_up_matrix, controller, manager, enable_double_press=True):
        self.active = False
        self.controller = controller
        self.manager = manager
        self.light_up_matrix = light_up_matrix
        self.enable_multiple_press = enable_double_press
        self.manager.register(self)

    def activate(self):
        self.active = True

    def indicate(self):
        self.send_matrix(self.light_up_matrix, interval=5)
    
    def deactivate(self):
        self.active = False
    
    def send_matrix(self, matrix, interval=2.0, fading=True):
        self.controller.display_matrix(matrix, interval=interval, fading=fading)

    def on_rotate(self, value):
        pass

    def on_multiple_press(self, value):
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
        self.subscriptions = []
        if WITHMQTT:
            self.client = mqtt.Client("Nuimo")
            self.client.on_message = self.on_message
            self.client.on_disconnect = self.reconnect_client
            self.client.on_connect = self.on_connect
            self.client.connect("localhost")
            self.client.loop_start()

        self.active: SubController = None
        self.active_index = -1
        self.submodules = []
        self.press_delay = 0.2
        self.already_pressed = 0
        self.already_released = False

    def change_active(self, increase_by=1):
        if self.active:
            self.active.deactivate()
            if isinstance(self.active, MQTTSubController) and WITHMQTT:
                for t in self.submodules[self.active_index][1]:
                    self.client.unsubscribe(t)
            self.active_index += increase_by
            self.active_index %= len(self.submodules)
            self.active = self.submodules[self.active_index][0]
            self.active.activate()
            self.active.indicate()
            if isinstance(self.active, MQTTSubController) and WITHMQTT:
                for t in self.submodules[self.active_index][1]:
                    self.client.subscribe(t)
        else:
            if self.submodules != []:
                self.active_index = 0
                self.active = self.submodules[0][0]
                self.active.activate()
                self.active.indicate()
                if isinstance(self.active, MQTTSubController) and WITHMQTT:
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
            self.active.activate()
            self.active.indicate()
            if isinstance(self.active, MQTTSubController) and WITHMQTT:
                for t in self.submodules[0][1]:
                    self.client.subscribe(t)

    def on_message(self, client, userdata, message):
        if isinstance(self.active, MQTTSubController):
            if message.on_topic in self.submodules[self.active_index][1]:
                self.active.on_message(message.on_topic, message.payload)

    def reconnect_client(self, client, userdata, rc):
        client.connect("localhost")

    def check_press(self, press_number):
        if self.already_pressed == press_number:
            if self.already_pressed == 1:
                self.already_pressed = 0
                self.active.on_press()
                if self.already_released:
                    self.active.on_release()
            else:
                self.already_pressed = 0
                self.active.on_multiple_press(self.already_pressed)

    def received_gesture_event(self, event):
        if not self.active:
            return
        val = event.gesture.value
        if not isinstance(val, int):
            val = val[0]
        if val == 1:  # button press
            if self.active.enable_multiple_press:
                self.already_pressed += 1
                Timer(self.press_delay, self.check_press, [self.already_pressed])
            else:
                self.active.on_press()
        elif val == 2:  # release
            if self.active.enable_multiple_press:
                if self.already_pressed == 0:
                    self.active.on_release()
                else:
                    self.already_released = True
            else:
                self.active.on_release()
        elif val >= 3 and val <= 6:  # SWIPE
            direction = Direction(val - 3)
            self.active.on_swipe(direction)
        elif val >= 8 and val <= 11:  # TOUCH
            direction = Direction(val - 8)
            if direction == Direction.BOTTOM:
                self.active.indicate()
            else:
                self.active.on_touch(direction)
        elif val >= 12 and val <= 15:  # LONGTOUCH
            direction = Direction(val - 12)
            if direction == Direction.LEFT:
                self.change_active(-1)
            elif direction == Direction.RIGHT:
                self.change_active(1)
            else:
                self.active.on_long_touch(direction)
        elif val == 16:  # ROTATION
            self.active.on_rotate(event.value)

    def on_connect(self, client, userdata, flags, rc):
        for s in self.subscriptions:
            client.subscribe(s[0])
    
    def publish(self, topic, payload, retained=False):
        if WITHMQTT:
            self.client.publish(topic, payload, retain=retained)

    def disconnect_succeeded(self):
        print("disconnected")
        self.controller.connect()

    def started_connecting(self):
        print("started connecting")

    def connect_succeeded(self):
        print("connect succeded")

    def connect_failed(self, error):
        print("connect failed", error)

    def started_disconnecting(self):
        print("started disconnecting")

class MQTTSubController(SubController):
    def __init__(self, light_up_matrix, controller, topics, manager):
        self.topics = topics
        super().__init__(light_up_matrix, controller, manager)
    
    def get_topics(self):
        return self.topics
    
    def on_message(self, topic, payload):
        pass

    def publish(self, topic, message):
        self.manager.publish(topic, message)
