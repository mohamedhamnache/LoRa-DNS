from utils.frame_utils import reverse_endian


class Frame:
    def __init__(
        self,
        sf,
        cr,
        snr,
        rssi,
        tmstp,
        mType,
        fCnt=None,
        joinEUI=None,
        devEUI=None,
        devNonce=None,
        devAddr=None,
        mic=None,
    ):
        self.sf = sf
        self.cr = cr
        self.snr = snr
        self.rssi = rssi
        self.fCnt = fCnt
        self.tmstp = tmstp
        self.timeOnAir = 0
        self.mType = mType
        self.devEUI = devEUI
        if self.mType == "JoinRequest":
            self.joinEUI = joinEUI
            self.devNonce = hex(int(devNonce)).split("x")[-1]
            self.MIC = mic
            self.PHYPayload = (
                "00"
                + reverse_endian(str(joinEUI))
                + reverse_endian(str(devEUI))
                + reverse_endian(str(self.devNonce))
                + self.MIC
            )
        else:
            self.devAddr = devAddr
