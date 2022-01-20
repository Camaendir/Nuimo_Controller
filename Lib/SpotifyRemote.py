from time import time

from .DeviceManager import Remote, Device, Direction
from Spotipy_Adapter import *
from matrices import *


class SpotifyRemote(Remote):

    def __init__(self, light_up_matrix=music_matrix, device_id="7a0dbf97d642f2b3138936c4286763ebe99fff9b", playlist_url="spotify:playlist:3NWvrg2ZiU43QoFc87brzl", enable_multiple_press=True, acceleration_curve="slow"):
        super().__init__(light_up_matrix, enable_multiple_press=enable_multiple_press)
        if acceleration_curve not in ("slow", "fast"):
            print("Spotify acceleration curve must be either 'slow' or 'fast'")
            print(f"Got {acceleration_curve}")
            print("Reverting to default acceleration curve 'slow'")
            acceleration_curve = "slow"
        self.acceleration_curve = acceleration_curve
        self.value = get_volume()
        self.playlist_url = playlist_url
        self.device_id = device_id
        self.timer = time()

    def on_rotate(self, value, device: Device):
        if time() - self.timer > 5:
            v = get_volume()
            if not v:
                device.send_matrix(self, stop_matrix, interval=1)
                return
            self.value = v
        if self.acceleration_curve == "slow":
            value = self.slow_acceleration_curve(value)
        else:
            value = self.fast_acceleration_curve(value)
        self.value += value
        self.value = min(100, self.value)
        self.value = max(0, self.value)
        success = set_volume(int(self.value))
        if not success:
            device.send_matrix(self, stop_matrix, interval=1)
        else:
            device.send_matrix(self, get_matrix_from_number(int(self.value)), interval=1, fading=True)
        self.timer = time()

    def on_press(self, device: Device):
        r = play_pause()
        if r == 0:
            device.send_matrix(self, pause_matrix)
        elif r == 1:
            device.send_matrix(self, play_matrix)
        else:
            device.send_matrix(self, stop_matrix)
    
    def on_multiple_press(self, value, device: Device):
        if value == 2:
            next_song()
            device.send_matrix(self, next_matrix)
        elif value == 3:
            previous_song()
            device.send_matrix(self, last_matrix)
    
    def on_long_touch(self, direction: Direction, device: Device):
        if direction == Direction.LEFT:
            previous_song()
            device.send_matrix(self, last_matrix)
        if direction == Direction.RIGHT:
            next_song()
            device.send_matrix(self, next_matrix)

    def on_swipe(self, direction, device: Device):
        if direction == Direction.LEFT:
            previous_song()
            device.send_matrix(self, last_matrix)
        elif direction == Direction.RIGHT:
            next_song()
            device.send_matrix(self, next_matrix)
        elif direction == Direction.TOP:
            transfer_to(self.device_id)
            device.send_matrix(self, loudspeaker_matrix)
        elif direction == Direction.BOTTOM:
            play_song_current_or_new_device(self.playlist_url, self.device_id)
            device.send_matrix(self, heart_matrix)
