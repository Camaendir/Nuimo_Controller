import nuimo
import threading
from Controller import *
from SpotifyController import SpotifyController

mac_use = 0
macs = ("dc:1c:77:d0:9a:d9", "CB:DB:5D:3E:34:6E")
manager = nuimo.ControllerManager(adapter_name='hci0')
print("Using Mac: ", macs[mac_use])
controller = nuimo.Controller(mac_address=macs[mac_use], manager=manager)
man = MQTTClientManager(controller)
controller.listener = man


class LumibaerController(BrightnessLightController):

    def __init__(self, indication_number, topic_prefix, controller, manager, additional_topics=None,
                 base_matrix=lightbulb_matrix):
        super().__init__(indication_number, topic_prefix, controller, manager, additional_topics=additional_topics,
                         base_matrix=base_matrix)
        self.colors = [wave_matrix, fire_matrix, ying_matrix, leaf_matrix]
        self.color_status = 0

    def on_swipe(self, direction: Direction):
        if direction == Direction.TOP:
            self.publish("room/lumibaer/status", 1)
            self.send_matrix(star_matrix, interval=3)
        elif direction == Direction.BOTTOM:
            self.publish("room/lumibaer/status", 0)
            self.send_matrix(lightbulb_matrix, interval=3)
        elif direction == Direction.RIGHT:
            self.color_status = (self.color_status + 1) % len(self.colors)
            self.publish("room/lumibaer/color/set", self.color_status)
            self.send_matrix(self.colors[self.color_status])
        elif direction == Direction.LEFT:
            self.color_status = (self.color_status - 1) % len(self.colors)
            self.publish("room/lumibaer/color/set", self.color_status)
            self.send_matrix(self.colors[self.color_status])


class SignController(BrightnessLightController):

    def on_swipe(self, direction: Direction):
        if direction == direction.TOP:
            self.publish("hall/sign/status", 1)
            self.send_matrix(snake_matrix, interval=3)
        elif direction == direction.BOTTOM:
            self.publish("hall/sign/status", 0)
            self.send_matrix(lightbulb_matrix, interval=3)
        else:
            super().on_swipe(direction)


SpotifyController(music_matrix, controller, man)
SignController(0, "hall/sign", controller, man, base_matrix=sign_matrix)
LumibaerController(1, "room/lumibaer", controller, man)
MatrixDisplayController(matrix_matrix, controller, "test/matrix", man)

controller.connect()
x = threading.Thread(target=manager.run)
x.start()
