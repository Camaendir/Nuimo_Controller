from Controller import BrightnessLightController, Direction, MQTTSubController
from matrices import *


class LumibaerController(BrightnessLightController):

    def __init__(self, indication_number, topic_prefix, controller, manager, additional_topics=tuple(),
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


class MatrixDisplayController(MQTTSubController):

    def __init__(self, light_up_matrix, controller, topic, manager, enable_multiple_press=False):
        super().__init__(light_up_matrix, controller, (topic,), manager, enable_multiple_press=enable_multiple_press)

    def on_message(self, topic, payload):
        self.send_matrix(payload.decode(), interval=5)
