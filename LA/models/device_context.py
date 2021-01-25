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
        self.dev_eui = dev_eui
        self.join_eui = join_eui
        self.dev_addr = dev_addr
        self.appSKey = appSKey
        self.fNwkSIntKey = fNwkSIntKey
        self.sNwkSIntKey = sNwkSIntKey
        self.nwkSEncKey = nwkSEncKey
        self.dev_nonce = dev_nonce
        self.join_req_type = join_req_type
