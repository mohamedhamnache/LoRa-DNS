import requests
import uuid
import datetime
from config import IP_ADDRESS, D_NAME
from models.network import Network
from db.models.db_network import DbNetwork
from db.models.db_device import DbDevice


class La_client:
    def register_network(self):
        url = "http://localhost:9106/api/networks"
        nwk = Network()
        payload = '{"dName":"' + nwk.dName + '", "ipAddr": "' + nwk.ip + '"}'
        headers = {"Content-Type": "application/json"}
        response = requests.request("POST", url, headers=headers, data=payload)
        # print(response.status_code)
        if response.status_code == 200:
            # print(response.json())
            r = response.json()
            nwk.net_id = r["Net_ID"]
            db_network = DbNetwork(
                nwk.dName, nwk.ip, nwk.net_id, datetime.datetime.now()
            )
            try:
                db_network.save_to_db()
                print("A new Network is Created Successfuly")
            except:
                print("The Added Network Can Not Be Saved to Database")
        else:
            print(response.json())

    def register_device(self, devEUI, appKey):
        network = DbNetwork.find_by_dname(D_NAME)

        if not network:
            return {"message": "Network does not exist"}
        net_id = network.Net_ID
        loop = True
        while loop:
            device_id = uuid.uuid1().hex[:8]
            joinEUI = str(net_id) + str(device_id)
            #print(joinEUI)
            if not DbDevice.find_by_joinEUI(joinEUI):
                loop = False

        device = DbDevice(devEUI, joinEUI, net_id, appKey, datetime.datetime.now())
        try:
            device.save_to_db()
            # print(device.devEUI)
            # print(device.joinEUI)
            # print(device.fNet_ID)
            print("A new Device is Created Successfuly")
        except:
            print("The Added Device Can Not Be Saved to Database")

    def dns_resolver(self, joinEUI, PHYPayload):
        url = "http://localhost:9106/api/dns-resolver"

        payload = (
            '{"join-eui":"'
            + joinEUI
            + '","dname_src":"'
            + D_NAME
            + '", "ip_src": "'
            + IP_ADDRESS
            + '", "PHYPayload": "'
            + PHYPayload
            + '"}'
        )

        headers = {"Content-Type": "application/json"}
        response = requests.request("GET", url, headers=headers, data=payload)
        print(response.text)


#la = La_client()
#la.register_network()
#la.register_device('BEEFDEAD0009DEA','BEEF456789ABCDEF0123456789ABCDEF')
#la.dns_resolver("fe5440fa627b60cc")
