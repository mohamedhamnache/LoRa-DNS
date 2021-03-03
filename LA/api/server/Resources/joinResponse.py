from flask_restful import Resource, reqparse

import json
import ast
from db.models.db_device import DbDevice
from clients.chs_client import Chs_client


class JoinResponseHandler(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("device",help="This field cannot be blank", required=True)
        parser.add_argument("context",help="This field cannot be blank", required=True)
        parser.add_argument("keys",help="This field cannot be blank", required=True)
        data = parser.parse_args()
        print(data)
        print('****** Data Parser *****')
        
        device = ast.literal_eval(data["device"])

        #print(device['deviceProfileID'])
        context = ast.literal_eval(data["context"])
        #print(context)
        keys = ast.literal_eval(data["keys"])
        #print(keys)
        chs_client = Chs_client()
        device_profile_id = chs_client.get_roaming_device_profile_id()
        
        if device_profile_id:
            device['device']['deviceProfileID'] = device_profile_id
            chs_client.create_device(device)
            chs_client.set_device_context(context)
            chs_client.set_device_keys(keys)
        
