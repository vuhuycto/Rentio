from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.report import ReportModel


class Report(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "user_id",
        type=int,
        required=True,
        help="This field cannot be left blank")

    # @jwt_required()
    def post(self, user_id):
        data = Report.parser.parse_args()

        if ReportModel.is_reported(user_id):
            return {"message": "This account is already reported"}, 400

        ReportModel.add_to_database(ReportModel(**data))
        return {"message": "This user is reported, please for judging"}, 200
