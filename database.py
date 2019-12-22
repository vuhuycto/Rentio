import os
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from multiprocessing.util import register_after_fork

engine = create_engine("postgresql+psycopg2://postgres:sesame@localhost:5432/rentio")
register_after_fork(engine, engine.dispose)

Base = declarative_base()
Session = sessionmaker(bind=engine)

session = Session()
