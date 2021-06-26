import spotipy
from spotipy.oauth2 import SpotifyOAuth
from time import sleep
from env import spotify_client_id, spotify_client_secret, spotify_redirect_url
from random import randint

scope = "user-read-playback-state,user-modify-playback-state,user-read-currently-playing,playlist-read-private"
sp = spotipy.Spotify(client_credentials_manager=SpotifyOAuth(scope=scope, client_id=spotify_client_id,
                                                             client_secret=spotify_client_secret,
                                                             redirect_uri=spotify_redirect_url, open_browser=False))


def transfer_to(id):
    sp.transfer_playback(id)


def get_volume():
    cp = sp.current_playback()
    if cp is None:
        return 0
    return cp["device"]["volume_percent"]


def set_volume(value):
    try:
        sp.volume(value)
        return True
    except spotipy.SpotifyException as e:
        return False


def next_song():
    sp.next_track()


def previous_song():
    sp.previous_track()


def is_playing():
    return sp.current_playback() is None


def play_pause():  # 0 -> pausing, 1 -> starting, 2 -> error
    cp = sp.current_playback()
    if cp is None:
        return 2
    if cp["is_playing"]:
        sp.pause_playback()
        return 0
    else:
        sp.start_playback()
        return 1


def play_song(context_url, device_id=None, random=False):
    if not random:
        sp.start_playback(context_uri=context_url, device_id=device_id)
    else:
        sp.start_playback(context_uri=context_url, device_id=device_id, offset=randint(0, 30)) # Random


def play_song_current_or_new_device(context_url, device_id, random=True):
    if sp.current_playback() is None:
        play_song(context_url, device_id, random=random)
    else:
        play_song(context_url, random=random)
