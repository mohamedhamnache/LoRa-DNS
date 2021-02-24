from flask_restful import Resource, reqparse
import requests
import json
from db.models.db_device import DbDevice
from pyThingPark.lorawan import JoinRequest

class JoinResponseHandler(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument(
            "device", help="This field cannot be blank", required=True
        )
        parser.add_argument(
            "context", help="This field cannot be blank", required=True
        )
        parser.add_argument("keys", help="This field cannot be blank", required=True)
        data = parser.parse_args()
        #print(data)
              
        