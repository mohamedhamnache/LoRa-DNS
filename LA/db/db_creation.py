from db_connection import engine, Base
from sqlalchemy import Column, String, Integer, Date, ForeignKey


# Session = sessionmaker(bind=engine)


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


class DbDevice(Base):

    __tablename__ = "Device"

    id = Column(Integer, primary_key=True, autoincrement=True)
    devEUI = Column(String(16), unique=True, nullable=False)
    joinEUI = Column(String(16), unique=True, nullable=False)
    fNet_ID = Column(String(8), ForeignKey("Network.Net_ID"))
    appKey = Column(String(32), unique=False, nullable=False)
    registered_on = Column(Date, nullable=False)
    # resolve = relationship("DNS")

    def __init__(self, devEUI, joinEUI, net_id, appKey, registered_on):
        self.devEUI = devEUI
        self.joinEUI = joinEUI
        self.fNet_ID = net_id
        self.appKey = appKey
        self.registered_on = registered_on


class DbDNS(Base):

    __tablename__ = "DNS"

    id = Column(Integer, primary_key=True, autoincrement=True)
    ipAddr = Column(String(15), unique=True, nullable=False)
    dName = Column(String(100), unique=True, nullable=False)
    fNet_ID = Column(String(8), ForeignKey("Network.Net_ID"))
    fdevEUI = Column(String(16), ForeignKey("Device.devEUI"))
    registered_on = Column(Date, nullable=False)

    def __init__(self, ipAddr, dName, net_id, devEUI, registered_on):
        self.ipAddr = ipAddr
        self.dName = dName
        self.fNet_ID = net_id
        self.fdevEUI = devEUI
        self.registered_on = registered_on


Base.metadata.create_all(bind=engine)
