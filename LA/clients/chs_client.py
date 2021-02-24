import requests
import json
import queue
from config import CHS_API_URL, CHS_USER, CHS_PASSWORD
from config import DEVICE_PROFILE_NAME, ORGANIZATION_ID, APPLICATION_ID
from models.frame import Frame

# from models.device_context import DeviceContext


motes = {}


class Chs_client:
    def __init__(self):
        self.url = CHS_API_URL
        self.username = CHS_USER
        self.password = CHS_PASSWORD
        self.devEuis = []
        self.token = None
        self.frames = queue.Queue()

    def connect(self):

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        # print(self.url + "/internal/login")

        data = (
            '{ "password": "'
            + self.password
            + '", \n   "email": "'
            + self.username
            + '" \n }'
        )

        # print(data)
        response = requests.post(
            self.url + "/internal/login", headers=headers, data=data
        )
        # print(response.content.decode())
        r = json.loads(response.content.decode())
        try:
            self.token = r["jwt"]
            # print(self.token)
        except:
            self.token = None
            raise Exception(r)

    def get_devices(self):
        self.devEuis = []
        self.devAddrs = {}
        if not self.token:
            self.connect()
        if not self.token:
            self.connect()
        headers = {
            "Accept": "application/json",
            "Grpc-Metadata-Authorization": "Bearer " + self.token,
        }
        params = (("limit", "100"),)
        response = requests.get(self.url + "/devices", headers=headers, params=params)
        r = json.loads(response.content.decode())
        for devs in r["result"]:
            if devs["devEUI"] not in self.devEuis:
                self.devEuis.append(devs["devEUI"])

    def check_valid_response(self, data, cpt=0):

        if cpt > 3:
            raise Exception(data)
        print(data)
        if "error" in data.keys():
            print(type(data["error"]))
            if data["code"] == 16:
                print("houra")
                self.token = None
                self.connect()
            else:
                raise Exception(json.dumps(data))
            return False
        else:
            return True

    def uplinkHandler(self, frame):
        uplinkTypes = ["UnconfirmedDataUp", "ConfirmedDataUp", "JoinRequest"]
        mType = frame["result"]["uplinkFrame"]["phyPayloadJSON"]["mhdr"]["mType"]
        if mType not in uplinkTypes:
            raise IgnoreFrame(mType)
        sf = frame["result"]["uplinkFrame"]["txInfo"]["loRaModulationInfo"][
            "spreadingFactor"
        ]
        cr = frame["result"]["uplinkFrame"]["txInfo"]["loRaModulationInfo"]["codeRate"][
            2:
        ]
        snr = frame["result"]["uplinkFrame"]["rxInfo"][0]["loRaSNR"]
        rssi = frame["result"]["uplinkFrame"]["rxInfo"][0]["rssi"]
        tmstp = frame["result"]["uplinkFrame"]["rxInfo"][0]["time"]
        ChMask = []
        for i in range(0, 4):
            ChMask.append(1)
        for j in range(5, 15):
            ChMask.append(0)

        if (
            not "fhdr"
            in frame["result"]["uplinkFrame"]["phyPayloadJSON"]["macPayload"].keys()
        ):
            # raise NotAJoinRequestHandler()
            print("This is a Join Request")
            joinEUI = frame["result"]["uplinkFrame"]["phyPayloadJSON"]["macPayload"][
                "joinEUI"
            ]
            devEUI = frame["result"]["uplinkFrame"]["phyPayloadJSON"]["macPayload"][
                "devEUI"
            ]
            devNonce = frame["result"]["uplinkFrame"]["phyPayloadJSON"]["macPayload"][
                "devNonce"
            ]
            mic = frame["result"]["uplinkFrame"]["phyPayloadJSON"]["mic"]

            # see tools.py in same dir
        if mType == "JoinRequest":
            genFrame = Frame(
                sf,
                cr,
                snr,
                rssi,
                tmstp,
                mType,
                joinEUI=joinEUI,
                devEUI=devEUI,
                devNonce=devNonce,
                mic=mic,
            )
        else:

            b64Payload = frame["result"]["uplinkFrame"]["phyPayloadJSON"]["macPayload"][
                "frmPayload"
            ][0]["bytes"]
            # dirty calculation of the size in bytes of the payload
            if b64Payload:
                payloadSize = len(b64Payload) * 3 / 4 - b64Payload.count("=", -2)
            else:
                payloadSize = 0
            if self.currentTxPow is not None:
                txPow = self.currentTxPow
            else:
                # TxPower set to maximum at initialization
                txPow = 14

            genFrame = Frame(sf, cr, snr, rssi, tmstp, mType, fCnt, devAddr)
        return genFrame

    def startFrameHandler(self, gatewayid, handlerUp):
        if not self.token:
            self.connect()
        headers = {
            "Accept": "application/json",
            "Grpc-Metadata-Authorization": "Bearer " + self.token,
        }

        with requests.get(
            self.url + "/gateways/" + gatewayid + "/frames",
            headers=headers,
            stream=True,
        ) as f:
            print(f)
            for l in f.iter_lines():
                if l:
                    decoded = l.decode()
                    trimmed = (
                        decoded.replace('\\"', '"')
                        .replace('"{', "{")
                        .replace('}"', "}")
                    )
                    data = json.loads(trimmed)
                    print(data)

                    # check if it is an error message
                    if self.check_valid_response(data):
                        # Updating known devices
                        self.get_devices()
                        print("[Check] Registered Devices are : ", self.devEuis)
                        if "uplinkFrame" in data["result"].keys():
                            genFrame = handlerUp(data)
                            print("[Check] check JoinReq Source")
                            if genFrame.devEUI not in self.devEuis:
                                self.frames.put(genFrame)
                                # print(genFrame)

    def get_device_context(self, dev_eui):
        if not self.token:
            self.connect()
        headers = {
            "Accept": "application/json",
            "Grpc-Metadata-Authorization": "Bearer " + self.token,
        }
        response = requests.get(
            self.url + "/devices/" + dev_eui + "/activation", headers=headers
        )
        context = json.loads(response.content.decode())
        context["deviceActivation"]["appSKey"] = "00000000000000000000000000000000"
        return context

    def get_device(self, devEUI):
        """
            Get device information 
            :devEUI
            :nwkKey
            :appKey
            :genAppKey
        """
        if not self.token:
            self.connect()
        headers = {
            "Accept": "application/json",
            "Grpc-Metadata-Authorization": "Bearer " + self.token,
        }
        url = self.url + "/devices/" + devEUI
        response = requests.get(url, headers=headers)
        device = json.loads(response.content.decode())["device"]
        return {"device": device}

    def get_device_keys(self, devEUI):
        if not self.token:
            self.connect()
        headers = {
            "Accept": "application/json",
            "Grpc-Metadata-Authorization": "Bearer " + self.token,
        }
        url = self.url + "/devices/" + devEUI + "/keys"
        response = requests.get(url, headers=headers)
        keys = json.loads(response.content.decode())
        keys["deviceKeys"]["appKey"] = "00000000000000000000000000000000"
        return keys

    def get_roaming_device_profile_id(self):
        params = (
            ("limit", "100"),
            ("offset", "1"),
            ("organizationID", ORGANIZATION_ID),
            ("applicationID", APPLICATION_ID),
        )
        if not self.token:
            self.connect()
        headers = {
            "Accept": "application/json",
            "Grpc-Metadata-Authorization": "Bearer " + self.token,
        }
        url = self.url + "/device-profiles"
        response = requests.get(url, headers=headers, params=params)
        profiles = json.loads(response.content.decode())
        for p in profiles['result']:
            if p['name'] == DEVICE_PROFILE_NAME:
                return p['id']
        return None

    def create_device(self, device):
        if not self.token:
            self.connect()
        headers = {
            "Accept": "application/json",
            "Grpc-Metadata-Authorization": "Bearer " + self.token,
        }
        devEUI = device["device"]["devEUI"]
        url = self.url + "/devices/" + devEUI
        response = requests.post(url, headers=headers, data=device)
        print(response.status_code)

    def set_device_context(self, context):
        """
            Set device context
        """
        if not self.token:
            self.connect()
        headers = {
            "Accept": "application/json",
            "Grpc-Metadata-Authorization": "Bearer " + self.token,
        }
        devEUI = context["deviceActivation"]["devEUI"]
        url = self.url + "/devices/" + devEUI
        response = requests.post(url, headers=headers, data=context)
        print(response.status_code)

    def set_device_keys(self, keys):
        """
            Set Device Keys
        """
        if not self.token:
            self.connect()
        headers = {
            "Accept": "application/json",
            "Grpc-Metadata-Authorization": "Bearer " + self.token,
        }
        devEUI = keys["deviceKeys"]["devEUI"]
        url = self.url + "/devices/" + devEUI + "/keys"
        response = requests.post(url, headers=headers, data=keys)
        print(response.status_code)


class UnknownDevice(Exception):
    pass


class NotAJoinRequestHandler(Exception):
    pass


class IgnoreFrame(Exception):
    pass


class InvalidSF(Exception):
    pass


class InvalidTxPow(Exception):
    pass


test = Chs_client()
# test.get_devices()
# print(test.devEuis)
# c = test.get_device_context("70b3d549967ceb93")
# print("devEUI: ", c.devEUI)
# print("devAddr : ", c.devAddr)
# test.connect()
#print(test.get_device("beefdead0009deaa"))
print(test.get_roaming_device_profile_id())
# print(test.get_device_keys('beefdead0009deaa'))
# print(test.get_device_context('beefdead0009deaa'))
