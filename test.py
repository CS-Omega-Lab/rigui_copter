from netifaces import interfaces, ifaddresses, AF_INET
key = '192.168'
for ifaceName in interfaces():
    addresses = [i['addr'] for i in ifaddresses(ifaceName).setdefault(AF_INET, [{'addr': 'No IP addr'}])]
    for addr in addresses:
        if key in addr:
            print(addr)
