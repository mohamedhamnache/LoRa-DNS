import requests
from models.network import Network


class La_client:
    def register_network(self):
        url = "http://localhost:9106/api/networks"
        nwk = Network()
        payload = '{"dName":"' + nwk.dName + '", "ipAddr": "' + nwk.ip + '"}'
        headers = {"Content-Type": "application/json"}
        response = requests.request("POST", url, headers=headers, data=payload)
        print(response.status_code)
        if response.status_code == 200:
            print(response.json())
            r =response.json()
            
            nwk.net_id = r ['Net_ID']
        else:
            print(response.json())


la = La_client()
la.register_network()
