from flask import Flask
from app import api_bp
from flask_cors import CORS
from Models import db, RevokedTokenModel

def create_app(config_filename):
    app = Flask(__name__)
    app.config.from_object(config_filename)
    app.register_blueprint(api_bp, url_prefix='/api')

    db.init_app(app)
    @app.before_first_request
    def create_tables():
        db.create_all()
    return app
    
    

if __name__ == "__main__":
    app = create_app("config")
    app.run(host='0.0.0.0',port =9106,debug=True)
