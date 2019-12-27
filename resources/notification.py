from flask_restful import Resource
from flask_jwt import jwt_required
from models.order import OrderModel


class RenterNotification(Resource):
    @jwt_required()
    def get(self, renter_id):
        orders = []
        for order in OrderModel.get_not_notified_orders(renter_id):
            order.set_notified()
            orders.append(order.json())
        return {"orders": orders}, 200


class LenderNotification(Resource):
    @jwt_required()
    def get(self, lender_id):
        return {"pending_requests": [request.json() for request in OrderModel.get_pending_requests(lender_id)]}, 200


class ExpiringNotification(Resource):
    @jwt_required()
    def get(self, renter_id):
        return {"expiring": [expiring_order.json() for expiring_order in OrderModel.get_expiring_orders(renter_id)]}, 200


class ExpiredNotification(Resource):
    @jwt_required()
    def get(self, renter_id):
        expired_orders = []
        for expired_order in OrderModel.get_expired_orders(renter_id):
            expired_order.set_expired()
            expired_orders.append(expired_order.json())
        return {"expired_orders": expired_orders}, 200