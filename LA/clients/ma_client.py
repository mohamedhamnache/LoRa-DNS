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

    def register_device(self):
        network = DbNetwork.find_by_dname(D_NAME)
        if not network:
            return {"message": "Network does not exist"}

        device = DbDevice(
            "DEADDEAD0009DEAA", "66b80c060009deaa", "66b80c06", datetime.datetime.now()
        )
        try:
            device.save_to_db()
            print("A new Device is Created Successfuly")
        except:
            print("The Added Device Can Not Be Saved to Database")

    def dns_resolver(self, joinEUI):
        url = "http://localhost:9106/api/dns-resolver"

        payload = '{"join-eui": "' + joinEUI + '"}'
        headers = {"Content-Type": "application/json"}
        response = requests.request("GET", url, headers=headers, data=payload)
        print(response.text)


la = La_client()
la.register_device()
# la.dns_resolver("e822bfaae822bfacd")
