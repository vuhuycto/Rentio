from sqlalchemy import Column, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database import Base, session


class ReportModel(Base):
    __tablename__ = "report"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    removed = Column(Boolean, nullable=True)

    user = relationship("UserModel", back_populates="report")

    @staticmethod
    def is_reported(user_id):
        return True if session.query(ReportModel).filter(ReportModel.user_id == user_id).first() else False

    @staticmethod
    def add_to_database(report):
        session.add(report)
        session.commit()
