from flask import Blueprint
from flask_restful import Api


api_bp = Blueprint("api", __name__)
api = Api(api_bp)

from Resources import network
from Resources import ma_dns

# Netwok Endpoints
api.add_resource(network.Network, "/networks")

# DNS Endpoints

api.add_resource(ma_dns.MA_dns, "/dns-resolver")
