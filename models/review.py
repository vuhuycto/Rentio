from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy import and_
from sqlalchemy.orm import relationship
from database import Base, session


class ReviewModel(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    comment = Column(String(100))
    star = Column(Integer)
    user_id = Column(Integer, ForeignKey("users.id"))

    product = relationship("ProductModel", back_populates="reviews")
    user = relationship("UserModel", back_populates="reviews")

    def json(self):
        return {
            "id": self.id,
            "product_id": self.product_id,
            "comment": self.comment,
            "star": self.star,
            "user_id": self.user_id
        }

    @staticmethod
    def is_reviewed_by(user_id, product_id):
        return True if session.query(ReviewModel).\
            filter(and_(ReviewModel.user_id == user_id, ReviewModel.product_id == product_id)).all() else False

    @staticmethod
    def search_from_database_by_product_id(product_id):
        return session.query(ReviewModel).filter(ReviewModel.product_id == product_id).all()

    @staticmethod
    def add_to_database(review):
        session.add(review)
        session.commit()
