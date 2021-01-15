from sqlalchemy import Column, String, Integer, Date, ForeignKey
from db_connection import Base, engine
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)
session = Session()


class DbDNS(Base):

    __tablename__ = "DNS"

    id = Column(Integer, primary_key=True, autoincrement=True)
    ipAddr = Column(String(15), unique=True, nullable=False)
    dName = Column(String(16), unique=True, nullable=False)
    fNet_ID = Column(String(8), ForeignKey("Network.Net_ID"))
    fdevAddr = Column(String(16), ForeignKey("Device.devAddr"))
    registered_on = Column(Date, nullable=False)

    def __init__(self, ipAddr, dName, net_id, devAddr, registered_on):
        self.ipAddr = ipAddr
        self.dName = dName
        self.fNet_ID = net_id
        self.fdevAddr = devAddr
        self.registered_on = registered_on

    def save_to_db(self):
        session.add(self)
        session.commit()
