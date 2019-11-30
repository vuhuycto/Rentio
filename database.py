import os
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship

engine = create_engine(os.environ.get("DATABASE_URL", "sqlite:///data.db"))
# engine = create_engine(os.environ.get("mysql+pymysql://root+sesame")

Base = declarative_base()
Session = sessionmaker(bind=engine)

session = Session()
