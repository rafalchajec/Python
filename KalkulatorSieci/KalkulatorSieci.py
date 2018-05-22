#!/usr/bin/python
import socket
import sys
import json
import ipaddress
from ipaddress import IPv4Address, IPv4Network


def toBinary(ipadd):
    ip = ipadd.split(".")
    address = '{0:08b}.{1:08b}.{2:08b}.{3:08b}'.format(int(ip[0]), int(ip[1]), int(ip[2]), int(ip[3]))
    return address

def val_IP(address):
    a = address.split('.')
    if len(a) != 4:
        return False
    for x in a:
        if not x.isdigit():
            return False
        i = int(x)
        if i < 0 or i > 255:
            return False
    return True


def val_Mask(mask):
    for x in mask:
        if not x.isdigit():
            return False
    maska = int(mask)
    if maska > 32 or maska < 1:
        return False
    return True





all = []
if len(sys.argv) < 2 or len(sys.argv) > 2:
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    mask = 24
    argPodany = ((str)(ip) + '/' + (str)(mask))
    sprawdzTab = [ip, mask]

else:
    argPodany = sys.argv[1]
    sprawdzTab = argPodany.split('/')
    print(sprawdzTab)

    if not val_IP(sprawdzTab[0]):
        print("Zły adres IP")
        sys.exit()
    if not val_Mask(sprawdzTab[1]):
        print("Zła maska podsieci")
        sys.exit()

# I Adres sieci

#ip i maske na binarny i robimy and

adres_1 = ipaddress.ip_interface(argPodany)
adrStr = "Adres sieci : {}".format(adres_1.network)
print(adrStr)
all.append(adrStr)

# II Klasę sieci

tabIP = sprawdzTab[0].split('.')
tabIPint = (int)(tabIP[0])

if tabIPint < 126:
    print("Adres klasy A")
    all.append("Adres klasy A")
elif 128 < tabIPint < 192:
    print("Adres klasy B")
    all.append("Adres klasy B")
elif 191 < tabIPint < 224:
    print("Adres klasy C")
    all.append("Adres klasy C")
elif 223 < tabIPint < 240:
    print("Adres klasy D")
    all.append("Adres klasy D")
else:
    print("Adres klasy E")
    all.append("Adres klasy E")

# III Maska sieci w formacie dziesiętnym (np. 255.255.255.0) i binarnym



mask = ipaddress.ip_network(adres_1.network)
adrStr = "Maska dziesietny: {}".format(mask.netmask)
print(adrStr)
all.append(adrStr)
binmask = str(mask.netmask)
adrStr = "Maska binarny: {}".format(toBinary(binmask))
print(adrStr)
all.append(adrStr)

# IV Adres broadcast (dziesiętnie i binarnie)

#Na postaci binarnej maski wykonujemy operację logiczną NOT

bnetwork = ((str)(adres_1.network)).split('/')
bcaststring = (bnetwork[0] + '/' + str(mask.netmask))
bcast = IPv4Network(bcaststring)
adrStr = "Broadcast dziesietny: {}".format(bcast.broadcast_address)
print(adrStr)
all.append(adrStr)

binbcast = (str)(bcast.broadcast_address)
adrStr = "Broadcast binarny: {}".format(toBinary(binbcast))
print(adrStr)
all.append(adrStr)

# V Minimalny adres hosta (dziesiętnie i binarnie)

# adres sieci + 1

numberOfIp = ipaddress.ip_network(adres_1.network)
adrStr = "Min host dziesietny: {}".format(adres_1.network[1])
print(adrStr)
all.append(adrStr)
fhost = (str)(adres_1.network[1])
adrStr = "Min host binarny: {}".format(toBinary(fhost))
print(adrStr)
all.append(adrStr)

# VI Maksymalny zakres hosta (dziesiętnie i binarnie)

#adres rozgłoszeniowy - 1

adrStr = "Max host dziesietny: {}".format(adres_1.network[numberOfIp.num_addresses - 2])
print(adrStr)
all.append(adrStr)
lhost = (str)(adres_1.network[numberOfIp.num_addresses - 2])
adrStr = "Max host binarny: {}".format(toBinary(lhost))
print(adrStr)
all.append(adrStr)

# VII Maksymalna ilość hostów, która może być przypisana do danej podsieci (dziesiętnie i binarnie 😊)

adrStr = "Dostepne adresy IP dziesietny: {}".format(numberOfIp.num_addresses - 2)
print(adrStr)
all.append(adrStr)
adrStr = "Dostepne adresy IP binarny: {}".format("{0:b}".format(numberOfIp.num_addresses - 2))
print(adrStr)
all.append(adrStr)


# ZAPISZ DO DŻEJSONA


dżejson = json.dumps(all)

with open('dżejson.json', 'w') as plik:
    for linia in dżejson:
        plik.write('\n'.join(str(line) for line in linia))
        if "," in linia:
            plik.write('\n')
