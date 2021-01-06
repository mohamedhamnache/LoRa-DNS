class Frame:
    def __init__(
        self,
        sf,
        cr,
        snr,
        rssi,
<<<<<<< HEAD
        tmstp,
        mType,
        fCnt=None,
=======
        fCnt,
        tmstp,
        mType,
>>>>>>> 41494cdcfdbffa23a9b5402d8be870fbecfb1ed0
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
        if self.mType == "JoinRequest":
            self.joinEUI = joinEUI
            self.devEUI = devEUI
            self.devNonce = devNonce
        else:
            self.devAddr = devAddr
