from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.pool import SingletonThreadPool

from ypd import config

Base = declarative_base()
engine = create_engine(config['db']['url'], connect_args={'check_same_thread': False}, poolclass=SingletonThreadPool)
Session = sessionmaker(bind=engine, expire_on_commit=False)