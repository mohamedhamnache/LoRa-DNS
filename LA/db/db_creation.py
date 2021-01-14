from db_connection import engine, Base
from db.models.db_device import DbDevice
from db.models.db_network import DbNetwork
from db.models.db_dns import DbDNS

Base.metadata.create_all(bind=engine)
#Session = sessionmaker(bind=engine)