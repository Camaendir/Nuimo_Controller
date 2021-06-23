import nuimo
import threading
import math
from time import sleep


VERBOSE = False
WITHOUTMQTT = True


if not WITHOUTMQTT:
    import paho.mqtt.client as mqtt
    import paho.mqtt.subscribe as subscribe


play_matrix = nuimo.LedMatrix(
    "".join(
        [
            "         ",
            "  *      ",
            "  **     ",
            "  ***    ",
            "  *****  ",
            "  ***    ",
            "  **     ",
            "  *      ",
            "         "
        ]
    )
)

pause_matrix = nuimo.LedMatrix(
    "".join(
        [" "*9] + ["  ** **  " for _ in range(7)] + [" "*9]
    )
)

next_symbol =     "".join(
        [
            "         ",
            "         ",
            "  *  *   ",
            "  ** *   ",
            "  ****   ",
            "  ** *   ",
            "  *  *   ",
            "         ",
            "         "
        ]
    )

next_matrix = nuimo.LedMatrix(
    next_symbol
)

last_matrix = nuimo.LedMatrix(
    next_symbol[::-1]
)

music_matrix = nuimo.LedMatrix(
    "".join([
        "  ***** *",
        "  *****  ",
        "  *   *  ",
        "  *   *  ",
        "  *   *  ",
        " **  **  ",
        "*** ***  ",
        " *   *   ",
        "         "
    ])
)

light_matrix = nuimo.LedMatrix(
    "".join([
        "    *    ",
        " *     * ",
        "         ",
        "    +    ",
        "+  +*+  +",
        "    +    ",
        "         ",
        " *     * ",
        "    *    "
    ])
)

matrix_list = (play_matrix, pause_matrix, next_matrix, last_matrix, music_matrix, light_matrix)


def print_ln(*args):
    if VERBOSE:
        print(*args)

def reconnect_client(client, userdata, rc):
    client.connect("localhost")


def update_matrix_volume(vol):
    rank = math.floor(81 / 100 * vol)
    matrix = nuimo.LedMatrix(" " * (81 - rank) + "*" * rank)
    controller.display_matrix(matrix, interval=2, fading=True)

def update_matrix_status(status):
    if status:
        controller.display_matrix(play_matrix, interval=5, fading=True)
    else:
        controller.display_matrix(pause_matrix, interval=5, fading=True)

def update_matrix_test(position):
    controller.display_matrix(matrix_list[position], interval=10, fading=False)

def on_message(client, userdata, message):
    print_ln("mqtt message recieved", message)
    if message.topic == "nuimo/spotify/volume/get":
        update_matrix_volume(int(message.payload))
    elif message.topic == "nuimo/spotify/status/get":
        update_matrix_status(message.payload != b"true")


def on_connect(client, userdata, flags, rc):
    client.subscribe("nuimo/spotify/volume/get")
    client.subscribe("nuimo/spotify/status/get")

class MQTTListener(nuimo.ControllerListener):

    def __init__(self):
        self.buffer = []
        self.matrix_position = 0
        self.running = False
        self.thread = threading.Thread(target=self.send_average)
        if WITHOUTMQTT:
            self.client = mqtt.Client("Nuimo")
            self.client.connect("localhost")
            self.client.on_message = on_message
            self.client.on_disconnect = reconnect_client
            self.client.on_connect = on_connect
            self.client.loop_start()

    def publish_volume_increase(self, volume):
        self.client.publish("spotify/volume/increase", str(volume))

    def send_play_pause(self):
        self.client.publish("spotify/play_state/set", "")

    def send_average(self):
        print_ln("send in 1 sec")
        sleep(0.2)
        print_ln("send now")
        val_sum = sum(self.buffer)
        self.buffer = []
        self.publish_volume_increase(val_sum // 60)
        print_ln("send via mqtt")
        self.thread = threading.Thread(target=self.send_average)
        self.running = False
        print_ln("reset variables")

    def received_gesture_event(self, event):
        if event.gesture == nuimo.Gesture.ROTATION:
            self.buffer.append(event.value)
            if not self.running:
                self.running = True
                self.thread.start()
        elif event.gesture == nuimo.Gesture.BUTTON_PRESS:
            self.send_play_pause()
        elif event.gesture == nuimo.Gesture.SWIPE_LEFT:
            self.matrix_position += 1 % len(matrix_list)
            update_matrix_test(self.matrix_position)
        elif event.gesture == nuimo.Gesture.SWIPE_RIGHT:
            self.matrix_position -= 1 % len(matrix_list)
            update_matrix_test(self.matrix_position)


    def started_connecting(self):
        print_ln("started connecting")

    def connect_succeeded(self):
        print_ln("connect successfully")

    def connect_failed(self, error):
        print_ln("connect failed", error)

    def started_disconnecting(self):
        print_ln("started disconnecting")

    def disconnect_succeeded(self):
        print_ln("disconnect succeeded")


manager = nuimo.ControllerManager(adapter_name='hci0')
print_ln("Using Mac: dc:1c:77:d0:9a:d9")
controller = nuimo.Controller(mac_address='dc:1c:77:d0:9a:d9', manager=manager)
controller.listener = MQTTListener()
controller.connect()
x = threading.Thread(target=manager.run)
x.start()
