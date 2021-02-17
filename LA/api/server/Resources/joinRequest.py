from flask_restful import Resource, reqparse
import requests
import json
from db.models.db_device import DbDevice
from pyThingPark.lorawan import JoinRequest
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
        data = parser.parse_args()
        #print(data)
        jr = JoinRequest.fromPayload(data['PHYPayload'])
        device = DbDevice.find_by_joinEUI(jr.JoinEUI)
        if device :
            mic = data['PHYPayload'] [-8:]
            computedMIC = jr.computeMIC(AppKey=device.appKey)
            if (mic == computedMIC):
                print("ok")
            else :
                return{"message" :"Invalide MIC"},300
        else :
            return {"message": "Device Not Found"},301         
        