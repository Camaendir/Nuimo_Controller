from time import time

from Controller import SubController
from Spotipy_Remote import *
from matrices import *


class SpotifyController(SubController):

    def __init__(self,  controller, manager, light_up_matrix=music_matrix, enable_multiple_press=False):
        super().__init__(light_up_matrix, controller, manager, enable_multiple_press=enable_multiple_press)
        self.value = get_volume()
        self.timer = time()

    def on_rotate(self, value):
        if time() - self.timer > 5:
            self.value = get_volume()
        sign = -1 if value < 0 else 1
        value = abs(value)
        value = pow(value, 1.6) * 0.00015
        self.value += (sign * value)
        self.value = min(100, self.value)
        self.value = max(0, self.value)
        self.send_matrix(get_matrix_from_number(int(self.value)), interval=1, fading=True)
        set_volume(int(self.value))
        self.timer = time()

    def on_press(self):
        r = play_pause()
        if r == 0:
            self.send_matrix(pause_matrix)
        elif r == 1:
            self.send_matrix(play_matrix)
        else:
            self.send_matrix(stop_matrix)

    def on_swipe(self, direction):
        if direction == direction.LEFT:
            previous_song()
            self.send_matrix(last_matrix)
        elif direction == direction.RIGHT:
            next_song()
            self.send_matrix(next_matrix)
        elif direction == direction.TOP:
            transfer_to("7a0dbf97d642f2b3138936c4286763ebe99fff9b")
            self.send_matrix(loudspeaker_matrix)
        elif direction == direction.BOTTOM:
            play_song_current_or_new_device("spotify:playlist:3NWvrg2ZiU43QoFc87brzl", "7a0dbf97d642f2b3138936c4286763ebe99fff9b")
            self.send_matrix(heart_matrix)
