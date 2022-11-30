import socket
import time

from netifaces import interfaces, ifaddresses, AF_INET


class AddressManager:
    def __init__(self, lgm):
        self.lgm = lgm

    def wait_for_network(self, subnet):
        self.lgm.dlg("ROBOT", 3, "Жду подключение с подсетью "+str(subnet)+"...")
        key = str(subnet)
        local_addr = None
        net_available = False
        while not net_available:
            for ifaceName in interfaces():
                addresses = [i['addr'] for i in ifaddresses(ifaceName).setdefault(AF_INET, [{'addr': 'No IP addr'}])]
                for addr in addresses:
                    if key in addr:
                        local_addr = addr
            if local_addr:
                net_available = True
                self.lgm.dlg("ROBOT", 3, "Сетевое подключение обнаружено.")
            time.sleep(1)

    def get_local_address_by_subnet(self, subnet):
        key = str(subnet)
        local_addr = None
        for ifaceName in interfaces():
            addresses = [i['addr'] for i in ifaddresses(ifaceName).setdefault(AF_INET, [{'addr': 'No IP addr'}])]
            for addr in addresses:
                if key in addr:
                    local_addr = addr
        if local_addr:
            return local_addr
        else:
            self.lgm.dlg('HOST', 1, 'Ошибка сетевого обнаружения, устройство не находится в указанной подсети.')
            return None

    def get_remote_address_by_name(self, name):
        det_name = str(name)
        try:
            #addr = socket.gethostbyname(det_name)
            addr = '192.168.31.16'
            return addr
        except Exception as e:
            self.lgm.dlg('HOST', 1, 'Ошибка сетевого обнаружения, RPI не в сети (' + str(e) + ')')
            return None
