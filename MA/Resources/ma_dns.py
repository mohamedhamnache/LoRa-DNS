import requests
from flask_restful import Resource, reqparse
from Models import NetworkModel

import json


class MA_dns(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument(
            "join-eui", help="This field cannot be blank", required=True
        )
        parser.add_argument("ip_src", help="This field cannot be blank", required=True)
        parser.add_argument(
            "dname_src", help="This field cannot be blank", required=True
        )
        parser.add_argument(
            "PHYPayload", help="This field cannot be blank", required=True
        )
        data = parser.parse_args()
        net_id = data["join-eui"][:8]
        ip_src = data["ip_src"]
        dname_src = data["dname_src"]
        PHYPayload = data["PHYPayload"]
        # print(data)
        # print(net_id)
        try:
            nwk = NetworkModel.find_by_netid(Net_ID=net_id)
            if nwk:

                # payload = '{"dname_src":"'+ dname_src+ '", "ip_src": "'+ ip_src+ '", "PHYPayload": "'+ PHYPayload + '"}'
                payload = (
                    '{"dname_src":"'
                    + dname_src
                    + '", "ip_src": "'
                    + ip_src
                    + '", "PHYPayload": "'
                    + PHYPayload
                    + '"}'
                )
                payload = json.loads(payload)
                # print(payload)
                url = "http://" + nwk.ipAddr + ":9000/api/joinrequest"
                # url = "http://localhost:9000/api/joinrequest"
                headers = {"Accept": "application/json"}
                response = requests.request("GET", url, headers=headers, data=payload)
                # print(response.status_code)
                if response.status_code == 200:
                    #print("Peer is Reachable")
                    return {"dName": nwk.dName, "ipAddr": nwk.ipAddr,}, 200
                else:
                    print("Peer Unreachable")
                    return 404
            else:
                return {"message": "Resource not found"}, 404
        except:

            return {"error": "An error occurred !"}, 500
