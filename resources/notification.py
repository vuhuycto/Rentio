from flask_restful import Resource
from flask_jwt import jwt_required
from models.order import OrderModel


class RenterNotification(Resource):
    @jwt_required()
    def get(self, renter_id):
        orders = []
        for order in OrderModel.get_not_notified_orders(renter_id):
            order.set_notified(order.product_id)
            orders.append(order.json())
        return {"orders": orders}, 200


class LenderNotification(Resource):
    @jwt_required()
    def get(self, lender_id):
        return {"pending_requests": [request.json() for request in OrderModel.get_pending_requests(lender_id)]}, 200
