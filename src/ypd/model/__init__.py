from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from ypd import config

Base = declarative_base()
engine = create_engine(config['db']['url'])
Session = sessionmaker(bind=engine)