from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.review import ReviewModel
from models.order import OrderModel


class Review(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "product_id",
        type=int,
        required=True,
        help="This field cannot be left blank")
    parser.add_argument(
        "comment",
        type=str,
        required=True,
        help="This field cannot be left blank")
    parser.add_argument(
        "star",
        type=float,
        required=True,
        help="This field cannot be left blank")
    parser.add_argument(
        "user_id",
        type=int,
        required=True,
        help="This field cannot be left blank")

    # @jwt_required()
    def get(self, product_id):
        return {"reviews": review.json() for review in ReviewModel.search_from_database_by_product_id(product_id)}, 200

    # @jwt_required()
    def post(self, product_id):
        data = Review.parser.parse_args()

        if not OrderModel.is_ordered_by(data["user_id"], product_id):
            return {"message": "You didn't rent this product yet"}, 400

        if ReviewModel.is_reviewed_by(data["user_id"], product_id):
            return {"message": "You have reviewed this product"}, 400

        ReviewModel.add_to_database(ReviewModel(**data))
        return {"message": "Product is successfully reviewed"}, 201
