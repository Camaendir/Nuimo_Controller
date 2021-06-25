import nuimo
from Controller import MQTTClientManager
import threading

def start_manager(mac=""):
    manager = nuimo.ControllerManager(adapter_name='hci0')
    controller = nuimo.Controller(mac_address=mac, manager=manager)
    man = MQTTClientManager(controller)
    controller.listener = man
    controller.connect()
    x = threading.Thread(target=manager.run)
    x.start()
    return man, controller
