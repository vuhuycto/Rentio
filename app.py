import os

from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authentication, identity
from database import Base, engine
from resources.person import User, UserRegister, Profile, UserList
from resources.product import Product, Catalog, PopularProduct, CatalogBasedProduct, ProductList
from resources.order import RequestedOrder, RequestedOrderList, ResponsedOrder, ResponsedOrderList
from resources.review import Review
from resources.report import Report
from resources.notification import RenterNotification, LenderNotification

app = Flask(__name__)
# app.secret_key = os.urandom(16)
api = Api(app)

jwt = JWT(app, authentication, identity)    # /auth

Base.metadata.create_all(engine)

from database import session
from models.product import CatalogModel
from models.person import AdminModel

catalog1 = CatalogModel(type="household", img_url="http://0.0.0.0/household")
catalog2 = CatalogModel(type="device", img_url="http://0.0.0.0/device")

admin = AdminModel(
    first_name="duy",
    last_name="le",
    gender="male",
    birthday="1998/03/04",
    email="duy0804@gmail.com",
    username="duy",
    password="123456",
    phone="2134560987",
    address="Hanoi")

session.add(admin)
session.add(catalog1)
session.add(catalog2)
session.commit()

api.add_resource(UserRegister, "/register")
api.add_resource(User, "/user/<string:username>")
api.add_resource(UserList, "/users")
api.add_resource(Profile, "/edit_profile")
api.add_resource(Product, "/api/products/posts/<string:name>")
api.add_resource(ProductList, "/api/products")
api.add_resource(PopularProduct, "/api/products/popular")
api.add_resource(CatalogBasedProduct, "/api/products/catalog/<string:catalog_type>")
api.add_resource(RequestedOrder, "/api/products/<int:product_id>/order/request")
api.add_resource(ResponsedOrder, "/api/products/<int:product_id>/order/response")
api.add_resource(RequestedOrderList, "/api/products/order/<int:user_id>/requests")
api.add_resource(ResponsedOrderList, "/api/products/order/<int:user_id>/responses")
api.add_resource(Review, "/api/reviews/<int:product_id>")
api.add_resource(Catalog, "/api/catalog")
api.add_resource(Report, "/api/report/<int:user_id>")
api.add_resource(RenterNotification, "/notification/renters/<int:renter_id>")
api.add_resource(LenderNotification, "/notification/lenders/<int:lender_id>")

if __name__ == '__main__':
    app.run(port=os.environ.get("PORT", 5000))

