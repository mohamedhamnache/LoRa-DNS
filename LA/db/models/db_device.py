from sqlalchemy import Column, String, Integer, Date, ForeignKey
from sqlalchemy.orm import relationship
from db.db_connection import Base, engine
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)
session = Session()


class DbDevice(Base):

    __tablename__ = "Device"

    id = Column(Integer, primary_key=True, autoincrement=True)
    devEUI = Column(String(16), unique=True, nullable=False)
    joinEUI = Column(String(16), unique=True, nullable=False)
    fNet_ID = Column(String(8), ForeignKey("Network.Net_ID"))
    registered_on = Column(Date, nullable=False)
    # resolve = relationship("DNS")

    def __init__(self, devEUI, joinEUI, net_id, registered_on):
        self.devEUI = devEUI
        self.joinEUI = joinEUI
        self.fNet_ID = net_id
        self.registered_on = registered_on

    def save_to_db(self):
        session.add(self)
        session.commit()
