from flask import Blueprint
from flask_restful import Api


api_bp = Blueprint("api", __name__)
api = Api(api_bp)

from Resources import network

# Netwok Endpoints
api.add_resource(network.Network, "/networks")
