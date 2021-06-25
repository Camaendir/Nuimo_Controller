from SpotifyController import SpotifyController
from NuimoManager import start_manager
from matrices import sign_matrix
from CustomController import SignController, LumibaerController

mac = "dc:1c:77:d0:9a:d9"

# start the manager
man, controller = start_manager(mac)

# register your Controller
SpotifyController(controller, man)
SignController(0, "hall/sign", controller, man, base_matrix=sign_matrix)
LumibaerController(1, "room/lumibaer", controller, man)
