from math import ceil
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.cmac import CMAC
from pyThingPark.lorawan import JoinRequest


def reverse_endian(hexastring):
    return "".join(
        reversed([hexastring[i : i + 2] for i in range(0, len(hexastring), 2)])
    )


joinEUI = "beef25dead25dead"
devEUI = "beefdead0009deaa"
devNonce = "7f4a"
# PHYPayload = "0001000171ac293df0bd2d6e6645d32301e2e2f98f810f"
appkey = "BEEF456789ABCDEF0123456789ABCDEF"

PHYPayload = (
    "00"
    + reverse_endian(joinEUI)
    + reverse_endian(devEUI)
    + reverse_endian(devNonce)
    + "7ab29335"
)
print(PHYPayload)


jr = JoinRequest.fromPayload(PHYPayload)
print(jr)
mic = jr.computeMIC(AppKey="BEEF456789ABCDEF0123456789ABCDEF")
print(mic)


def computeMIC(AppKey):
    cmac = CMAC(algorithms.AES(bytes.fromhex(AppKey)), backend=default_backend())
    cmac.update(bytes.fromhex(PHYPayload[:-8]))
    MIC = cmac.finalize().hex()[:8]
    return MIC


# print(computeMIC(appkey))
