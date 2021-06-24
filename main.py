import nuimo
import threading
from Controller import *


mac_use = 0
macs = ("dc:1c:77:d0:9a:d9", "CB:DB:5D:3E:34:6E")
manager = nuimo.ControllerManager(adapter_name='hci0')
print("Using Mac: ", macs[mac_use])
controller = nuimo.Controller(mac_address=macs[mac_use], manager=manager)
man = MQTTClientManager(controller)
controller.listener = man

SpotifyController(music_matrix, controller, man)
BrightnessLightController(2, "hall/sign", controller, man)
BrightnessLightController(1, "room/lumibaer", controller, man)

print("connecting ...")
controller.connect()
x = threading.Thread(target=manager.run)
x.start()
