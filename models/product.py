from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey
from sqlalchemy import and_, func
from sqlalchemy.orm import relationship
from sqlalchemy.sql import label
from database import Base, session
from models.review import ReviewModel


class ProductModel(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    img_vid_url = Column(String(100))
    status = Column(Boolean)
    address = Column(String(50))
    daily_price = Column(Float, nullable=True)
    weekly_price = Column(Float, nullable=True)
    monthly_price = Column(Float, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("UserModel", back_populates="products")
    reviews = relationship("ReviewModel", back_populates="product", lazy="dynamic")
    catalogs = relationship("CatalogModel", secondary="product_catalog_rel")
    order = relationship("OrderModel", back_populates="product")

    def __repr__(self):
        return "<Product id={}, status={}, daily price={}, weekly price={}, monthly price={}>".\
            format(self.id, self.status, self.daily_price, self.weekly_price, self.monthly_price)

    def json(self):
        return {
            "id": self.id,
            "name": self.name,
            "img_vid_url": self.img_vid_url,
            "status": self.status,
            "address": self.address,
            "daily_price": self.daily_price,
            "weekly_price": self.weekly_price,
            "monthly_price": self.monthly_price,
            "user_id": self.user_id
        }

    @staticmethod
    def search_from_database_by_name(name):
        return session.query(ProductModel).filter(ProductModel.name == name).all()

    @staticmethod
    def search_from_database_by_id(product_id):
        return session.query(ProductModel).filter(ProductModel.id == product_id).first()

    @staticmethod
    def search_from_database_by_catalog(catalog_type):
        return session.query(ProductModel).\
            filter(and_(ProductModel.id == ProductCatalogRelationship.product_id,
                        CatalogModel.id == ProductCatalogRelationship.catalog_id,
                        CatalogModel.type == catalog_type)).all()

    @staticmethod
    def update_status(product_id, status):
        session.query(ProductModel).filter(ProductModel.id == product_id).\
            update({ProductModel.status: status}, synchronize_session=False)
        session.commit()

    @staticmethod
    def get_popular_products():
        return session.query(
                ProductModel.id,
                ProductModel.name,
                ProductModel.img_vid_url,
                ProductModel.status,
                ProductModel.address,
                ProductModel.daily_price,
                ProductModel.weekly_price,
                ProductModel.monthly_price,
                ProductModel.user_id,
                label("average_star", func.sum(ReviewModel.star) / func.count(ReviewModel.product_id))).\
            join(ReviewModel, ProductModel.id == ReviewModel.product_id).\
            group_by(
                ProductModel.id,
                ProductModel.name,
                ProductModel.img_vid_url,
                ProductModel.status,
                ProductModel.address,
                ProductModel.daily_price,
                ProductModel.weekly_price,
                ProductModel.monthly_price,
                ProductModel.user_id).\
            having(func.sum(ReviewModel.star) / func.count(ReviewModel.product_id) >= 4).\
            all()

    @staticmethod
    def get_all_products():
        return session.query(ProductModel).all()

    @staticmethod
    def add_to_database_by_catalog(product, catalog):
        catalog.products.append(product)
        session.commit()


class CatalogModel(Base):
    __tablename__ = "catalogs"

    id = Column(Integer, primary_key=True)
    type = Column(String(50), unique=True)
    img_url = Column(String(100))

    products = relationship("ProductModel", secondary="product_catalog_rel")

    def json(self):
        return {
            "id": self.id,
            "type": self.type,
            "img_url": self.img_url
        }

    def __repr__(self):
        return "<Catalog id={}, type={}>".\
            format(self.id, self.type)

    @staticmethod
    def search_from_database_by_type(catalog_type):
        return session.query(CatalogModel).filter(CatalogModel.type == catalog_type).first()

    @staticmethod
    def get_all():
        return session.query(CatalogModel).all()


class ProductCatalogRelationship(Base):
    __tablename__ = "product_catalog_rel"

    product_id = Column(Integer, ForeignKey("products.id"), primary_key=True)
    catalog_id = Column(Integer, ForeignKey("catalogs.id"), primary_key=True)
