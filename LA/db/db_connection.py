from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

# from sqlalchemy.ext.automap import automap_base
from config import DB_URL

engine = create_engine(DB_URL, echo=False)
Base = declarative_base()
