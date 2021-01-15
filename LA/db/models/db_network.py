from sqlalchemy import Column, String, Integer, Date
from sqlalchemy.orm import relationship
from db.db_connection import Base, engine
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)
session = Session()


class DbNetwork(Base):

    __tablename__ = "Network"

    id = Column(Integer, primary_key=True, autoincrement=True)
    dName = Column(String(100), unique=True, nullable=False)
    ipAddr = Column(String(15), unique=True, nullable=False)
    Net_ID = Column(String(8), unique=True, nullable=False)
    registered_on = Column(Date, nullable=False)
    # belong = relationship("Device")

    def __init__(self, dName, ipAddr, net_id, registered_on):
        self.dName = dName
        self.ipAddr = ipAddr
        self.Net_ID = net_id
        self.registered_on = registered_on

    def save_to_db(self):
        session.add(self)
        session.commit()

    @classmethod
    def return_all_Networks(cls):
        def to_json(x):
            return {
                "id": x.id,
                "dName": x.dName,
                "ipAddr": x.ipAddr,
                "Net_ID": x.Net_ID,
                "registered_on": str(x.registered_on),
            }

        return {
            "Networks": list(map(lambda x: to_json(x), session.query(DbNetwork).all()))
        }

    @classmethod
    def find_by_dname(cls, dName):
        return session.query(DbNetwork).filter_by(dName=dName).first()
