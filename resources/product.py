from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.product import ProductModel, CatalogModel
from models.person import UserModel


class Product(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "name",
        type=str,
        required=True,
        help="This field cannot be left blank")
    parser.add_argument(
        "address",
        type=str,
        required=True,
        help="This field cannot be left blank")
    parser.add_argument(
        "daily_price",
        type=float,
        required=True,
        help="This field cannot be left blank")
    parser.add_argument(
        "weekly_price",
        type=float,
        required=True,
        help="This field cannot be left blank")
    parser.add_argument(
        "monthly_price",
        type=float,
        required=True,
        help="This field cannot be left blank")
    parser.add_argument(
        "catalog_type",
        type=str,
        required=True,
        help="This field cannot be left blank")
    parser.add_argument(
        "user_id",
        type=int,
        required=True,
        help="This field cannot be left blank")

    def get(self, name):
        return {"products": [product.json() for product in ProductModel.search_from_database_by_name(name)]}, 200

    @jwt_required()
    def post(self, name):
        data = Product.parser.parse_args()
        data.update({"status": False})

        catalog = CatalogModel.search_from_database_by_type(data["catalog_type"])
        del data["catalog_type"]

        ProductModel.add_to_database_by_catalog(ProductModel(**data), catalog)

        product = sorted(
            ProductModel.search_from_database_by_name(data["name"]),
            key=lambda product: product.id)[-1]
        username = UserModel.search_from_database_by_id(data["user_id"]).username
        url = "http://192.168.2.107:8080/" + username + "/" + str(product.id)
        product.update_img_url(url)

        return {
            "message": "Product posted successfully",
            "img_vid_url": url
        }, 201


class PostedProduct(Resource):
    def get(self, product_id):
        return ProductModel.search_from_database_by_id(product_id).json(), 200


class PopularProduct(Resource):
    def get(self):
        products = []
        for product_id, name, img_vid_url, \
                status, address, daily_price, weekly_price, \
                monthly_price, user_id, average_star in ProductModel.get_popular_products():
            product = {
                "product_id": product_id,
                "name": name,
                "img_vid_url": img_vid_url,
                "status": status,
                "address": address,
                "daily_price": daily_price,
                "weekly_price": weekly_price,
                "monthly_price": monthly_price,
                "user_id": user_id,
                "average_star": float(average_star)}
            products.append(product)
        return {"products": products}, 200


class CatalogBasedProduct(Resource):
    def get(self, catalog_type):
        return {"products": [product.json() for product in ProductModel.search_from_database_by_catalog(catalog_type)]}


class ProductList(Resource):
    def get(self):
        return {"products": [product.json() for product in ProductModel.get_all_products()]}, 200


class Catalog(Resource):
    def get(self):
        return {"catalogs": [catalog.json() for catalog in CatalogModel.get_all()]}, 200
