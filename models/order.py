import datetime

from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey
from sqlalchemy import and_
from sqlalchemy.orm import relationship
from database import Base, session


class OrderModel(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    start_date = Column(Date)
    end_date = Column(Date)
    lender_national_id = Column(String(12))
    renter_national_id = Column(String(12), nullable=True)
    bank_number = Column(String(14))
    lender_id = Column(Integer, ForeignKey("users.id"))
    renter_id = Column(Integer, ForeignKey("users.id"))
    accepted = Column(Boolean, nullable=True)
    expired = Column(Boolean, nullable=True)
    notified = Column(Boolean, nullable=True)

    product = relationship("ProductModel", back_populates="order")
    lender = relationship("UserModel", foreign_keys=[lender_id])
    renter = relationship("UserModel", foreign_keys=[renter_id])

    def __repr__(self):
        return "<Order id={}, product={}, start date={}, end date={}, lender_national_id={}, renter_national_id={}, " \
               "bank_number={}, lender={}, renter={}, accepted={}>". \
            format(
                self.id,
                self.product,
                self.start_date,
                self.end_date,
                self.lender_national_id,
                self.renter_national_id,
                self.bank_number,
                self.lender,
                self.renter,
                self.accepted)

    def json(self):
        return {
            "id": self.id,
            "product_id": self.product_id,
            "start_date": self.start_date.\
                strftime("%Y/%m/%d") if isinstance(self.start_date, datetime.date) else self.start_date,
            "end_date": self.end_date.\
                strftime("%Y/%m/%d") if isinstance(self.end_date, datetime.date) else self.end_date,
            "lender_national_id": self.lender_national_id,
            "renter_national_id": self.renter_national_id,
            "bank_number": self.bank_number,
            "lender_id": self.lender_id,
            "renter_id": self.renter_id,
            "accepted": self.accepted,
            "expired": self.expired,
            "notified": self.notified
        }

    def set_notified(self):
        session.query(OrderModel).filter(OrderModel.product_id == self.product_id).\
            update({"notified": True}, synchronize_session=False)
        session.commit()

    def set_expired(self):
        session.query(OrderModel).filter(OrderModel.id == self.id).\
            update({"expired": True}, synchronize_session=False)
        session.commit()

    @staticmethod
    def is_ordered_by(user_id, product_id):
        return True if session.query(OrderModel). \
            filter(and_(OrderModel.renter_id == user_id, OrderModel.product_id == product_id)).all() else False

    @staticmethod
    def search_requested_from_database_by_id(product_id):
        return session.query(OrderModel). \
            filter(and_(OrderModel.product_id == product_id, OrderModel.accepted == None)).first()

    @staticmethod
    def search_requested_orders_from_database_by_user(user_id):
        return session.query(OrderModel).filter(OrderModel.lender_id == user_id).all()

    @staticmethod
    def search_responsed_orders_from_database_by_user(user_id):
        return session.query(OrderModel).filter(OrderModel.renter_id == user_id).all()

    @staticmethod
    def get_all_requests_from_database():
        return session.query(OrderModel).filter(OrderModel.accepted == None).all()

    @staticmethod
    def search_order_from_database_by_id(product_id):
        return session.query(OrderModel).filter(OrderModel.product_id == product_id).first()

    @staticmethod
    def update_order(data):
        session.query(OrderModel).filter(OrderModel.product_id == data["product_id"]).\
            update(data, synchronize_session=False)
        session.commit()

    @staticmethod
    def get_all_orders():
        return session.query(OrderModel).all()

    @staticmethod
    def get_not_notified_orders(renter_id):
        return session.query(OrderModel).\
            filter(and_(OrderModel.renter_id == renter_id, OrderModel.notified == False)).all()

    @staticmethod
    def get_expiring_orders(renter_id):
        return session.query(OrderModel).\
            filter(and_(OrderModel.end_date - datetime.date.today() <= 3,
                        OrderModel.end_date - datetime.date.today() >= 1,
                        OrderModel.renter_id == renter_id)).all()

    @staticmethod
    def get_expired_orders(renter_id):
        return session.query(OrderModel).\
            filter(and_(OrderModel.end_date - datetime.date.today() <= 0,
                        OrderModel.renter_id == renter_id,
                        OrderModel.expired == False)).all()

    @staticmethod
    def get_pending_requests(lender_id):
        return session.query(OrderModel).\
            filter(and_(OrderModel.lender_id == lender_id, OrderModel.accepted == None)).all()

    @staticmethod
    def add_to_database(order):
        session.add(order)
        session.commit()
