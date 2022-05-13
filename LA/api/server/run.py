from flask import Flask
from app import api_bp
#import flask_monitoringdashboard as dashboard
#from flask_cors import CORS
from config import PORT


def create_app(config_filename):
    app = Flask(__name__)
    #dashboard.bind(app)
    app.config.from_object(config_filename)
    app.register_blueprint(api_bp, url_prefix="/api")
    return app

app = create_app("config")
if __name__ == "__main__":
    
    app.run(host="0.0.0.0", port=PORT, debug=False,threaded=True)
