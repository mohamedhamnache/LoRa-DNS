from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from config import DB_URL

engine = create_engine(DB_URL, echo =True)
Base = declarative_base()



