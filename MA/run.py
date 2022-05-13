from flask import Flask
from app import api_bp
#from flask_cors import CORS
#import flask_monitoringdashboard as dashboard
from Models import db


def create_app(config_filename):
    app = Flask(__name__)
    #dashboard.bind(app)
    app.config.from_object(config_filename)
    app.register_blueprint(api_bp, url_prefix="/api")

    db.init_app(app)

    @app.before_first_request
    def create_tables():
        db.create_all()

    return app

app = create_app("config")
if __name__ == "__main__": 
    app.run(host="0.0.0.0", port=9106, debug=False,threaded=True)
