import os
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from multiprocessing.util import register_after_fork

# engine = create_engine("postgresql+psycopg2://postgres:sesame@localhost:5432/rentio")
# engine = create_engine(os.environ.get("DATABASE_URL", "sqlite:///data.db"))
engine = create_engine(os.environ.get("postgres://rbllcgxtmntvhu:ad16fdf39b9cb08a798452e4bf2ab374ab15863748ab41ed6125331a1f937dd7@ec2-46-137-187-23.eu-west-1.compute.amazonaws.com:5432/dc7htujnbptmm9", "sqlite:///data.db"))
register_after_fork(engine, engine.dispose)

Base = declarative_base()
Session = sessionmaker(bind=engine)

session = Session()
