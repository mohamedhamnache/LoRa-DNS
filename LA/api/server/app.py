from flask import Blueprint
from flask_restful import Api


api_bp = Blueprint("api", __name__)
api = Api(api_bp)

from Resources import joinRequest
from Resources import joinResponse
api.add_resource(joinRequest.JoinRequestHandler, "/joinrequest")
api.add_resource(joinRequest.JoinResponseHandler, "/joinresponse")
