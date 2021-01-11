from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import DB_URL

engine = create_engine(DB_URL)
Session = sessionmaker(bind=engine)

Connector = declarative_base()

