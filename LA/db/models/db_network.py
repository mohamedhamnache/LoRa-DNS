from sqlalchemy import Column, String, Integer, Date
from sqlalchemy.orm import relationship
from db_connection import Base


class DbNetwork(Base):

    __tablename__ = "Network"

    id = Column(Integer, primary_key=True, autoincrement=True)
    dName = Column(String(100),unique=True, nullable=False)
    name = Column(String(100),unique=True, nullable=False)
    ipAddr = Column(String(15),unique=True, nullable=False)
    Net_ID = Column(String(15),unique=True, nullable=False)
    registered_on = Column(Date,nullable=False)
    belong = relationship("Device")
    

    def __init__(self, dName, ipAddr,net_id,registered_on):
        self.dName = dName
        self.ipAddr = ipAddr
        self.Net_ID = net_id
        self.registered_on = registered_on
        
