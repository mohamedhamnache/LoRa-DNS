from flask_sqlalchemy import *
import datetime

db = SQLAlchemy()


class NetworkModel(db.Model):
    __tablename__ = "LA_Roaming_NW"

    ID_RNW = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Net_ID = db.Column(db.String(120), unique=True, nullable=False)
    dName = db.Column(db.String(120), unique=True, nullable=False)
    ipAddr = db.Column(db.String(120), unique=True, nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_dname(cls, dName):
        return cls.query.filter_by(dName=dName).first()

    @classmethod
    def return_all(cls):
        def to_json(x):
            return {
                "ID_RNW": x.ID_RNW,
                "Net_ID": x.Net_ID,
                "dName": x.dName,
                "ipAddr": x.ipAddr,
                "registered_on": str(x.registered_on),
            }

        return {"networks": list(map(lambda x: to_json(x), NetworkModel.query.all()))}
