import os
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(os.environ.get("DATABASE_URL", "sqlite:///data.db"))

Base = declarative_base()
Session = sessionmaker(bind=engine)

session = Session()
