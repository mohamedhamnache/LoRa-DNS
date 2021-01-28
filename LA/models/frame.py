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
            self.devNonce = devNonce
            self.MIC = mic
            self.PHYPayload = (
                "00"
                + reverse_endian(joinEUI)
                + reverse_endian(devEUI)
                + reverse_endian(devNonce)
                + self.MIC
            )
        else:
            self.devAddr = devAddr
