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
        else:
            self.devAddr = devAddr
