import uuid
import datetime
from flask_restful import Resource, reqparse
from Models import NetworkModel

parser = reqparse.RequestParser()
parser.add_argument("dName", help="This field cannot be blank", required=True)
parser.add_argument("ipAddr", help="This field cannot be blank", required=True)


class Network(Resource):
    def get(self):
        return NetworkModel.return_all()

    def post(self):
        data = parser.parse_args()
        print(data)

        if NetworkModel.find_by_dname(data["dName"]):
            return (
                {
                    "message": "Network with Domaine Name {} already exists".format(
                        data["dName"]
                    )
                },
                409,
            )
        elif NetworkModel.find_by_ipaddr(data["ipAddr"]):
            return (
                {
                    "message": "Network with IP Address {} already exists".format(
                        data["ipAddr"]
                    )
                },
                409,
            )
        else:
            loop = True
            while loop:
                net_id = uuid.uuid1().hex[:8]
                if not NetworkModel.find_by_netid(net_id):
                    loop = False

        new_network = NetworkModel(
            Net_ID=net_id,
            dName=data["dName"],
            ipAddr=data["ipAddr"],
            registered_on=datetime.datetime.now(),
        )

        try:
            new_network.save_to_db()
            return {
                "message": "Network with Domaine Naame {} was created".format(
                    data["dName"]
                ),
                "Net_ID": net_id,
            }
        except:
            return {"message": "Something went wrong"}, 500
