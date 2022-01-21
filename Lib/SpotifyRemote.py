from time import time

from .DeviceManager import Remote, Device, Direction
from Spotipy_Adapter import *
from matrices import *


class SpotifyRemote(Remote):

    def __init__(self, device_id, playlist_url, light_up_matrix=music_matrix, enable_multiple_press=True, acceleration_curve="slow"):
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


class MultiplePlaylistSpotifyRemote(SpotifyRemote):
    def __init__(self, device_id, playlists_urls, playlist_matrices, selection_timeout=5, light_up_matrix=music_matrix, acceleration_curve="slow", enable_multiple_press=True):
        super().__init__(light_up_matrix=light_up_matrix, device_id=device_id, playlist_url=None, enable_multiple_press=enable_multiple_press, acceleration_curve=acceleration_curve)
        self.playlists_urls = playlists_urls
        self.playlist_matrices = playlist_matrices
        self.selects_playlist = False
        self.playlist_index = 0
        self.timer = -1
        self.selection_timeout = selection_timeout
        self.selection_value = 0

    def on_press(self, device: Device):
        self.check_reset()
        if self.selects_playlist:
            play_song_current_or_new_device(self.playlists_urls[self.playlist_index], self.device_id)
            self.reset_selection()
        else:
            super().on_press(device)

    def on_long_touch(self, direction: Direction, device: Device):
        self.check_reset()
        if not self.selects_playlist:
            super().on_long_touch(direction, device)

    def on_multiple_press(self, value, device: Device):
        self.check_reset()
        if not self.selects_playlist:
            super().on_multiple_press(value, device)

    def check_reset(self):
        if self.selects_playlist and time() - self.timer > self.selection_timeout:
            self.reset_selection()
            return True
        return False

    def reset_selection(self):
        print("Reset select")
        self.selects_playlist = False
        self.playlist_index = 0
        self.timer = -1

    def change_selection(self, amount, device: Device):
        print("Change seletion")
        self.playlist_index += amount
        self.playlist_index = self.playlist_index % len(self.playlists_urls)
        device.send_matrix(self, self.playlist_matrices[self.playlist_index])

    def on_rotate(self, value, device: Device):
        self.check_reset()
        if self.selects_playlist:
            self.timer = time()
            self.selection_value += value
            if self.selection_value > 200:
                self.change_selection(1, device)
                self.selection_value = 0
            if self.selection_value < -200:
                self.change_selection(-1, device)
                self.selection_value = 0
            print(self.selection_value)
        else:
            super().on_rotate(value, device)

    def on_swipe(self, direction, device: Device):
        self.check_reset()
        if direction == Direction.BOTTOM:
            if not self.selects_playlist:
                self.selects_playlist = True
                device.send_matrix(self, self.playlist_matrices[self.playlist_index])
                self.timer = time()
        elif direction == Direction.TOP:
            if self.selects_playlist:
                self.reset_selection()
            else:
                super().on_swipe(direction, device)
        else:
            super().on_swipe(direction, device)
