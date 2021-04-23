from network import LoRa
import socket
import time
import ubinascii

# Initialise LoRa in LORAWAN mode.
# Please pick the region that matches where you are using the device:
# Asia = LoRa.AS923
# Australia = LoRa.AU915
# Europe = LoRa.EU868
# United States = LoRa.US915
lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.EU868, adr=True)

# create an OTAA authentication parameters
dev_eui = ubinascii.unhexlify("BEEFDEAD0009DEAC")
app_eui = ubinascii.unhexlify("63bb9e78fafe4214")
app_key = ubinascii.unhexlify("BEEF456789ABCDEF0123456789ABCDEF")


def join(lora, app_eui, app_key):
    lora.join(activation=LoRa.OTAA, auth=(dev_eui, app_eui, app_key), timeout=0, dr=0)
    i = 0
    while not lora.has_joined() and i < 8:
        time.sleep(3)
        print("Try " + str(i) + " Not yet joined...")
        i += 1
    if i == 8:
        # print("Join failed !")
        print("retry join")
        join(lora, app_eui, app_key)


# join a network using OTAA (Over the Air Activation)
join(lora, app_eui, app_key)


# create a LoRa socket
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

# set the LoRaWAN data rate
s.setsockopt(socket.SOL_LORA, socket.SO_DR, 0)

# make the socket blocking
# (waits for the data to be sent and for the 2 receive windows to expire)
def send_data():
    s.setblocking(True)
    # send some data
    s.setblocking(False)
    s.send(bytes([0]))
    lora.stats()
    time.sleep(5)
    while 1:
        datarate = lora.stats().sftx
        pwridx = lora.stats().tx_power
        if lora.stats().snr >= 0:
            snr_sign = 0
        else:
            snr_sign = 1

        snr_val = int(abs(lora.stats().snr) * 10)
        if lora.stats().rssi >= 0:
            rssi_sign = 0
        else:
            rssi_sign = 1
        rssi_val = int(abs(lora.stats().rssi))
        print(lora.stats())
        print(bytes([datarate, pwridx, snr_sign, snr_val, rssi_val, rssi_sign]))
        s.send(bytes([datarate, pwridx, snr_sign, snr_val, rssi_val, rssi_sign]))
        data = s.recv(64)
        time.sleep(5)


# send_data()
# make the socket non-blocking
# (because if there's no data received it will block forever...)

# get any data received (if any...)
