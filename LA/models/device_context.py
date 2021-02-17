class DeviceContext:
    def __init__(
        self,
        dev_eui,
        join_eui,
        dev_addr,
        appSKey,
        fNwkSIntKey,
        sNwkSIntKey,
        nwkSEncKey,
        dev_nonce,
        join_req_type,
    ):
        self.devEUI = dev_eui
        self.joinEUI = join_eui
        self.devAddr = dev_addr
        self.appSKey = appSKey
        self.fNwkSIntKey = fNwkSIntKey
        self.sNwkSIntKey = sNwkSIntKey
        self.nwkSEncKey = nwkSEncKey
        self.devNonce = dev_nonce
        self.join_req_type = join_req_type
