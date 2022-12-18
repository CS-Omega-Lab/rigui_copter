import socket
import time

from netifaces import interfaces, ifaddresses, AF_INET


class AddressManager:
    def __init__(self, lgm, config):
        self.lgm = lgm
        self.config = config
        self.mode = True if config['network']['platform_addr_select'] == 'auto' else False

    def wait_for_network(self):
        key = str(self.config['network']['common_subnet'])
        if self.mode:
            self.lgm.dlg("PLTF", 3, "Режим сети: автоопределение адреса платформы")
        else:
            self.lgm.dlg("PLTF", 3, "Режим сети: статический адрес платформы")
        self.lgm.dlg("PLTF", 3, "Жду подключение с подсетью " + key + "...")
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
                self.lgm.dlg("PLTF", 3, "Сетевое подключение обнаружено.")
            time.sleep(1)

    def get_local_address_by_subnet(self):
        key = str(self.config['network']['common_subnet'])
        local_addr = None
        for ifaceName in interfaces():
            addresses = [i['addr'] for i in ifaddresses(ifaceName).setdefault(AF_INET, [{'addr': 'No IP addr'}])]
            for addr in addresses:
                if key in addr:
                    local_addr = addr
        if local_addr:
            return local_addr
        else:
            self.lgm.dlg('PLTF', 1, 'Ошибка сетевого обнаружения, устройство не находится в указанной подсети.')
            return None

    def get_remote_address_by_name(self, name):
        if self.mode:
            self.lgm.dlg("CNTR", 3,
                         "Определяю адрес платформы, подсеть: " + self.config['network']['common_subnet'])
        else:
            self.lgm.dlg("CNTR", 3, "Статический адрес платформы: " + self.config['network']['platform_static_addr'])
        det_name = str(name)
        try:
            if self.mode:
                addr = socket.gethostbyname(det_name)
            else:
                addr = self.config['network']['platform_static_addr']
            return addr
        except Exception as e:
            self.lgm.dlg('CNTR', 1, 'Ошибка сетевого обнаружения, RPI не в сети (' + str(e) + ')')
            return None
