import requests
import json

from config import CHS_API_URL, CHS_USER, CHS_PASSWORD
from models.frame import Frame
from models.device_context import DeviceContext


motes = {}


class Chs_client:
    def __init__(self):
        self.url = CHS_API_URL
        self.username = CHS_USER
        self.password = CHS_PASSWORD
        self.devEuis = []
        self.token = None

    def connect(self):

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        print(self.url + "/internal/login")

        data = (
            '{ "password": "'
            + self.password
            + '", \n   "email": "'
            + self.username
            + '" \n }'
        )
        print(data)
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
            # see tools.py in same dir
        if mType == "JoinRequest":
            genFrame = Frame(sf, cr, snr, rssi, tmstp, joinEUI, devEUI, devNonce)
        else:
            genFrame = Frame(sf, cr, snr, rssi, fCnt, tmstp, devAddr)
        return genFrame

        """
        if devAddr in motes.keys():
            # checking if any packetloss
            print("[DEBUG] LastFrameCounter=" + str(motes[devAddr].lastFrameCounter) + " | fCnt =" + str(fCnt))
            if motes[devAddr].lastFrameCounter == fCnt - 1:
                # no loss
                #motes[devAddr].lastFrame = genFrame
                #motes[devAddr].lastFrameCounter = fCnt
                # check if spreading factor value is correct
                if 7 <= sf <= 12:
                    # store the frames data per device address for ADR processing
                    motes[devAddr].framesLog[fCnt] = [snr, sf, txPow, rssi]
                # reset frames history upon communication reinit
                if fCnt == 0:
                    motes[devAddr].framesLog.clear()
                # act when frames history is complete
                if len(motes[devAddr].framesLog) == self.adrLog:
                    # execute adr
                    callAdr = adr.adr(motes[devAddr].framesLog)
                    newParameters = callAdr.anotherADR()
                    print("[OUTPUT ADR] SF=" + str(newParameters[0]) + " | TX_IDX=" + str(newParameters[1]))
                    self.sendUpdate(newParameters[0], newParameters[1], ChMask, devAddr)
                    # reset frames history
                    motes[devAddr].framesLog.clear()
                    # reset loss counter
                    motes[devAddr].sumPacketsLoss = 0
            else:
                # loss, if loss limit is reached, worst case parameters are sent
                print("[DEBUG] PACKET LOSS !!!")
                motes[devAddr].sumPacketsLoss += 1
                motes[devAddr].lastFrame.simulatedTimeOnAir = timeOnAir * (fCnt - motes[devAddr].lastFrameCounter)
                motes[devAddr].lastFrameCounter = fCnt
                if motes[devAddr].sumPacketsLoss >= 10:
                    self.sendUpdate(12, 1, ChMask, devAddr)
        else:
            motes[devAddr] = mote(devAddr, fCnt, genFrame)
        # return genFrame
        """

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
                        self.getDevEui()

                        if "uplinkFrame" in data["result"].keys():
                            genFrame = handlerUp(data)
                            print(genFrame)
                            """
                            try:
                                handlerUp(data)
                            except UnknownDevice as e:
                                print("[NET ERROR] Device " + str(e) + " not registered with our gateway")
                            except NotAJoinRequestHandler:
                                print("[PY ERR] JoinRequest passed in UplinkHandler")
                            except IgnoreFrame as e:
                                print("[NET ERROR] Frame " + str(e) + " in UplinkHandler")
                            except InvalidSF as e:
                                print("[ADR ERROR] Trying to update with SF=" + str(e))
                            except InvalidTxPow as e:
                                print("[ADR ERROR] Trying to update with PwrIdx=" + str(e))
                            except:
                                print("[PY ERR] Unable to decode following uplink message :" + str(data))
                                traceback.print_exc()
                        else:
                            try:
                                handlerDown(data)
                            except:
                                print("[PY ERR] Unable to decode following downlink message :" + str(data))
                    else:
                        self.startFrameHandler(gatewayid, handlerUp, handlerDown)
                    """

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
        context = json.loads(response.content.decode())["deviceActivation"]
        devEUI = context["devEUI"]
        devAddr = context["devAddr"]
        appSKey = context["appSKey"]
        nwkSEncKey = context["nwkSEncKey"]
        sNwkSIntKey = context["sNwkSIntKey"]
        fNwkSIntKey = context["fNwkSIntKey"]
        context = DeviceContext(
            devEUI,
            None,
            devAddr,
            appSKey,
            fNwkSIntKey,
            sNwkSIntKey,
            nwkSEncKey,
            None,
            None,
        )
        return context


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
test.get_devices()
print(test.devEuis)
test.get_device_context("70b3d549967ceb93")
