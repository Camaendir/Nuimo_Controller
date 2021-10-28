from Lib.DeviceManager import *
from Lib.SpotifyRemote import SpotifyRemote
from Lib.MQTTLightRemote import SignRemote, JSONLightRemote
from Lib.HTTPLightRemote import LumibaerRemote

mac1 = "dc:1c:77:d0:9a:d9"
mac2 = "f1:06:78:1e:34:4e"

manager = DeviceManager()

device1 = Device(manager, mac1, "Table - Black")
device2 = Device(manager, mac2, "Desk - White")

spotify = SpotifyRemote()
#lumibaer = LumibaerRemote(1, "192.168.178.32")
#sign = SignRemote(0, "hall/sign", manager)
kater = JSONLightRemote(0, "ha/kater/set", "ha/kater/is", manager)
#test = TestRemote()

device1.register_remotes([spotify, kater]), 
device2.register_remotes([spotify, kater])

manager.run()
