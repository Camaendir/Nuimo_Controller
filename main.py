from NuimoController.DeviceManager import *
from NuimoController.SpotifyRemote import MultiplePlaylistSpotifyRemote
from NuimoController.MQTTLightRemote import JSONLightRemote, LumibaerRemote
from matrices import f_2_matrix, monoid_matrix, phi_matrix, clock_matrix

mac1 = "dc:1c:77:d0:9a:d9"
mac2 = "f1:06:78:1e:34:4e"

manager = DeviceManager()

device1 = Device(manager, mac1, "Table - Black")
device2 = Device(manager, mac2, "Desk - White")

playlists = [
    "spotify:playlist:5ZKHZjpBcr33a2N4BiCXcj",
    "spotify:playlist:5TBB1TZbQ6p5uZgxAbp1Ar",
    "spotify:playlist:5clM7DxcYmOfTfDRbTKyJh",
]

matrices = [
    phi_matrix,
    monoid_matrix,
    f_2_matrix,
]

spotify = MultiplePlaylistSpotifyRemote(playlist_matrices=matrices, playlists_urls=playlists, device_id="7a0dbf97d642f2b3138936c4286763ebe99fff9b")
kater = JSONLightRemote(0, "ha/kater/set", "ha/kater/is", manager, base_matrix=clock_matrix)
lumibaer = LumibaerRemote(manager)

device1.register_remotes([spotify, lumibaer])
device2.register_remotes([spotify, kater, lumibaer])

manager.run()
