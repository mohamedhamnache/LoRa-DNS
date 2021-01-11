from flask_restful import Resource, reqparse
from Models import NetworkModel


class MA_dns(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument(
            "join-eui", help="This field cannot be blank", required=True
        )
        data = parser.parse_args()
        net_id = data["join-eui"][:8]
        # print(net_id)
        try:
            nwk = NetworkModel.find_by_netid(Net_ID=net_id)
            if nwk:
                print(nwk.dName)
                return {"dName": nwk.dName, "ipAddr": nwk.ipAddr,}, 200
            else:
                return {"message": "Resource not found"}, 404
        except:
            return {"error": "An error occurred !"}, 500
