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
            return {
                "message": "Network with Domaine Name {} already exists".format(
                    data["dName"]
                )
            }

        new_network = NetworkModel(
            Net_ID="11223",
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
                "Net_ID": Net_ID,
            }
        except:
            return {"message": "Something went wrong"}, 500
