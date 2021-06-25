import nuimo
from Controller import MQTTClientManager
import threading
from time import sleep


class ControllerManagerPrintListener(nuimo.ControllerManagerListener):
    def __init__(self, manager):
        self.mac = False
        self.manager = manager
        super().__init__()

    def controller_discovered(self, controller):
        print("Discovered Nuimo controller", controller.mac_address)
        self.mac = controller.mac_address
        self.manager.stop()


def start_manager(mac=""):
    if mac == "":
        print("no Mac present!\nTrying to find a Controller")
        manager = nuimo.ControllerManager(adapter_name='hci0')
        provider = ControllerManagerPrintListener(manager)
        manager.listener = provider
        manager.start_discovery()
        x = threading.Thread(target=manager.run)
        x.start()
        while not provider.mac:
            sleep(1)
        mac = provider.mac
        print("Using Mac:", mac)
        x.join()
        manager = nuimo.ControllerManager(adapter_name='hci0')
        controller = nuimo.Controller(mac_address=mac, manager=manager)
        man = MQTTClientManager(controller)
        controller.listener = man
        controller.connect()
        x = threading.Thread(target=manager.run)
        x.start()
        return man, controller

    manager = nuimo.ControllerManager(adapter_name='hci0')
    controller = nuimo.Controller(mac_address=mac, manager=manager)
    man = MQTTClientManager(controller)
    controller.listener = man
    controller.connect()
    x = threading.Thread(target=manager.run)
    x.start()
    return man, controller
