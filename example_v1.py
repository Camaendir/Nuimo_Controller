from version1.DeviceManager import *
from version1.SpotifyRemote import SpotifyRemote
from version1.MQTTLightRemote import SignRemote, LumibaerRemote

mac1 = "dc:1c:77:d0:9a:d9"
mac2 = "f1:06:78:1e:34:4e"

manager = DeviceManager()

device1 = Device(manager, mac1, "Table - Black")
device2 = Device(manager, mac2, "Desk - White")

spotify = SpotifyRemote()
lumibaer = LumibaerRemote(1, "room/lumibaer", manager)
sign = SignRemote(0, "hall/sign", manager)


device1.register_remotes([spotify, lumibaer, sign])
device2.register_remotes([spotify, lumibaer, sign])

manager.run()
