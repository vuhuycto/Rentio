from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship

engine = create_engine("mysql+pymysql://root:sesame@localhost:3306/test")

Base = declarative_base()
Session = sessionmaker(bind=engine)

session = Session()
