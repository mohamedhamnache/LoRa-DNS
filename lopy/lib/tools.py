from network import LoRa
import ubinascii

lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.EU868)


def get_devEUI():
    devEUI = ubinascii.hexlify(lora.mac()).upper().decode("utf-8")
    print(devEUI)
    return devEUI


get_devEUI()
