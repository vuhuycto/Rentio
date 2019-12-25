import datetime

from sqlalchemy import Column, Integer, String, Date, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import func
from sqlalchemy.sql import label
from database import Base, session
from models.product import ProductModel
from models.review import ReviewModel
from models.order import OrderModel
from models.report import ReportModel


class Person:
    def __init__(self, id, first_name, last_name, email, username, password, phone, address=None, gender=None,
                 birthday=None, **kwargs):
        super().__init__(**kwargs)
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.gender = gender
        self.birthday = birthday
        self.email = email
        self.username = username
        self.password = password
        self.phone = phone
        self.address = address


class AdminModel(Base, Person):
    __tablename__ = "admins"

    id = Column(Integer, primary_key=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    gender = Column(String(6))
    birthday = Column(Date)
    email = Column(String(50))
    username = Column(String(50))
    password = Column(String(16))
    phone = Column(String(10))
    address = Column(Text)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __repr__(self):
        return "<Admin id={}, name={}, gender={}, birthday={}, phone={}, address={}>". \
            format(self.id, self.first_name + self.last_name, self.gender, self.birthday, self.phone, self.address)

    @staticmethod
    def search_from_database_by_username(username):
        return session.query(AdminModel).filter(AdminModel.username == username).first()

    @staticmethod
    def search_from_database_by_id(user_id):
        return session.query(AdminModel).filter(AdminModel.id == user_id).first()


class UserModel(Base, Person):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    gender = Column(String(10), nullable=True)
    birthday = Column(Date, nullable=True)
    email = Column(String(50), unique=True)
    username = Column(String(50))
    password = Column(String(16))
    phone = Column(String(10))
    address = Column(Text, nullable=True)
    job = Column(String(50), nullable=True)
    free_trial_start = Column(Date, nullable=True)
    free_trial_end = Column(Date, nullable=True)

    products = relationship("ProductModel", back_populates="user", lazy="dynamic")
    reviews = relationship("ReviewModel", back_populates="user", lazy="dynamic")
    report = relationship("ReportModel", back_populates="user")

    def __init__(self, job=None, free_trial_start=None, free_trial_end=None, **kwargs):
        super().__init__(**kwargs)
        self.job = job
        self.free_trial_start = free_trial_start
        self.free_trial_end = free_trial_end

    def __repr__(self):
        return "<User id={}, name={}, gender={}, birthday={}, phone={}, address={}>". \
            format(self.id, self.first_name + self.last_name, self.gender, self.birthday, self.phone, self.address)

    def update_attributes(self, **kwargs):
        self.__dict__.update(**kwargs)

    def json(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "gender": self.gender,
            "birthday": self.birthday.\
                strftime("%Y/%m/%d") if isinstance(self.birthday, datetime.date) else self.birthday,
            "email": self.email,
            "username": self.username,
            "password": self.password,
            "phone": self.phone,
            "address": self.address,
            "job": self.job,
            "free_trial_start": self.free_trial_start.\
                strftime("%Y/%m/%d") if isinstance(self.free_trial_start, datetime.date) else self.free_trial_start,
            "free_trial_end": self.free_trial_end.\
                strftime("%Y/%m/%d") if isinstance(self.free_trial_end, datetime.date) else self.free_trial_end
        }

    @staticmethod
    def search_from_database_by_username(username):
        return session.query(UserModel).filter(UserModel.username == username).first()

    @staticmethod
    def search_from_database_by_id(user_id):
        return session.query(UserModel).filter(UserModel.id == user_id).first()

    @staticmethod
    def get_all_user():
        return session.query(UserModel).all()

    @staticmethod
    def get_top_lender():
        return session.query(
                UserModel.id,
                UserModel.first_name,
                UserModel.last_name,
                UserModel.gender,
                UserModel.birthday,
                UserModel.email,
                UserModel.username,
                UserModel.password,
                UserModel.phone,
                UserModel.address,
                UserModel.job,
                UserModel.free_trial_start,
                UserModel.free_trial_end,
                label("average_star", func.sum(ReviewModel.star) / func.count(ReviewModel.product_id))).\
            join(ProductModel, UserModel.id == ProductModel.user_id).\
            join(ReviewModel, ProductModel.id == ReviewModel.product_id). \
            group_by(
                UserModel.id,
                UserModel.first_name,
                UserModel.last_name,
                UserModel.gender,
                UserModel.birthday,
                UserModel.email,
                UserModel.username,
                UserModel.password,
                UserModel.phone,
                UserModel.address,
                UserModel.job,
                UserModel.free_trial_start,
                UserModel.free_trial_end). \
            having(func.sum(ReviewModel.star) / func.count(ReviewModel.product_id) >= 4). \
            all()

    @staticmethod
    def add_to_database(user):
        session.add(user)
        session.commit()

    @staticmethod
    def update_to_database(user):
        session.query(UserModel).filter(UserModel.username == user.username). \
            update({UserModel.__dict__[k]: v for k, v in user.json().items()}, synchronize_session=False)
        session.commit()
