from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.order import OrderModel
from models.product import ProductModel


class RequestedOrder(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "product_id",
        type=int,
        required=True,
        help="This field cannot be left blank")
    parser.add_argument(
        "start_date",
        type=str,
        required=True,
        help="This field cannot be left blank")
    parser.add_argument(
        "end_date",
        type=str,
        required=True,
        help="This field cannot be left blank")
    parser.add_argument(
        "lender_national_id",
        type=str,
        required=True,
        help="This field cannot be left blank")
    parser.add_argument(
        "bank_number",
        type=str,
        required=True,
        help="This field cannot be left blank")
    parser.add_argument(
        "lender_id",
        type=int,
        required=True,
        help="This field cannot be left blank")
    parser.add_argument(
        "renter_id",
        type=int,
        required=True,
        help="This field cannot be left blank")

    @jwt_required()
    def get(self, product_id):
        requested = OrderModel.search_requested_from_database_by_id(product_id)

        if not requested:
            return {"message": "This product is either ordered or not ordered"}, 400

        return requested.json(), 200

    @jwt_required()
    def post(self, product_id):
        data = RequestedOrder.parser.parse_args()

        if OrderModel.search_requested_from_database_by_id(product_id):
            return {"message": "This product has been ordered"}, 400

        data.update({"renter_national_id": None, "accepted": None})

        OrderModel.add_to_database(OrderModel(**data))

        return {"message": "Order has been successfully delivered to the lender"}, 201


class RequestedOrderList(Resource):
    @jwt_required()
    def get(self, user_id):
        return {"requested_orders":
                    [product.json() for product in OrderModel.search_requested_orders_from_database_by_user(user_id)]}, 200


class ResponsedOrder(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "product_id",
        type=int,
        required=True,
        help="This field cannot be left blank")
    parser.add_argument(
        "start_date",
        type=str,
        required=True,
        help="This field cannot be left blank")
    parser.add_argument(
        "end_date",
        type=str,
        required=True,
        help="This field cannot be left blank")
    parser.add_argument(
        "lender_national_id",
        type=str,
        required=True,
        help="This field cannot be left blank")
    parser.add_argument(
        "renter_national_id",
        type=str,
        required=True,
        help="This field cannot be left blank")
    parser.add_argument(
        "bank_number",
        type=str,
        required=True,
        help="This field cannot be left blank")
    parser.add_argument(
        "lender_id",
        type=int,
        required=True,
        help="This field cannot be left blank")
    parser.add_argument(
        "renter_id",
        type=int,
        required=True,
        help="This field cannot be left blank")
    parser.add_argument(
        "accepted",
        type=bool,
        required=True,
        help="This field cannot be left blank")

    @jwt_required()
    def get(self, product_id):
        return OrderModel.search_order_from_database_by_id(product_id).json(), 200

    @jwt_required()
    def post(self, product_id):
        data = ResponsedOrder.parser.parse_args()

        if not data["accepted"]:
            return {"message": "Your request has been denied"}, 400

        data.update({"notified": False, "expired": False})

        OrderModel.update_order(data)

        ProductModel.search_from_database_by_id(data["product_id"]).update_status(data["accepted"])

        return {"message": "The lender has been accepted your request"}, 200


class ResponsedOrderList(Resource):
    @jwt_required()
    def get(self, user_id):
        return {"orders":
                    [order.json() for order in OrderModel.search_responsed_orders_from_database_by_user(user_id)]}, 200
