from version0.SpotifyController import SpotifyController
from version0.NuimoManager import start_manager
from matrices import sign_matrix, matrix_matrix
from version0.CustomController import SignController, LumibaerController,MatrixDisplayController

mac = "dc:1c:77:d0:9a:d9"

# start the manager
manager, controller = start_manager(mac)

# register your Controller
SpotifyController(controller, manager)
SignController(0, "hall/sign", controller, manager, base_matrix=sign_matrix)
LumibaerController(1, "room/lumibaer", controller, manager)

# Test your Matrices with this Controller
MatrixDisplayController(matrix_matrix, controller, manager, "test/matrix")
