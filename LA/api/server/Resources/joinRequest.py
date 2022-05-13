from flask_restful import Resource, reqparse
import requests
import json
from db.models.db_device import DbDevice
from pyThingPark.lorawan import JoinRequest
from clients.chs_client import Chs_client
from api.client.joinResponseClient import joinResponseClient


class JoinRequestHandler(Resource):
    def get(self): 
        parser = reqparse.RequestParser()
        parser.add_argument(
            "PHYPayload", help="This field cannot be blank", required=True
        )
        parser.add_argument("ip_src", help="This field cannot be blank", required=True)
        parser.add_argument(
            "dname_src", help="This field cannot be blank", required=True
        )
        #print('mohamed 1')
        data = parser.parse_args()
        #print('mohamed 2')
        #print(data)
        if data["PHYPayload"]:

            jr = JoinRequest.fromPayload(data["PHYPayload"])
            device = DbDevice.find_by_joinEUI(jr.JoinEUI)
            if device:
                #print(device)
                mic = data["PHYPayload"][-8:]
                computedMIC = jr.computeMIC(AppKey=device.appKey)
                if mic == computedMIC:
                    #print("MIC ok")
                    #print(jr.DevEUI)
                    chs_client = Chs_client()
                    device_info = chs_client.get_device(jr.DevEUI)
                    #print(device_info)
                    context = chs_client.get_device_context(jr.DevEUI)
                    #print(context)
                    device_keys = chs_client.get_device_keys(jr.DevEUI)
                    #print(device_keys)
                    #print(data)
                    joinResponseClient(
                        data["ip_src"], 9000, device_info, context, device_keys
                    )
                else:
                    return {"message": "Invalide MIC"}, 300
            else:
                return {"message": "Device Not Found"}, 301
