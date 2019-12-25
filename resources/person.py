from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.person import UserModel


class User(Resource):
    @jwt_required()
    def get(self, username):
        return UserModel.search_from_database_by_username(username).json(), 200


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "first_name",
        type=str,
        required=True,
        help="This field cannot be left blank")
    parser.add_argument(
        "last_name",
        type=str,
        required=True,
        help="This field cannot be left blank")
    parser.add_argument(
        "phone",
        type=str,
        required=True,
        help="This field cannot be left blank")
    parser.add_argument(
        "email",
        type=str,
        required=True,
        help="This field cannot be left blank")
    parser.add_argument(
        "username",
        type=str,
        required=True,
        help="This field cannot be left blank.")
    parser.add_argument(
        "password",
        type=str,
        required=True,
        help="This field cannot be left blank.")

    def post(self):
        data = UserRegister.parser.parse_args()
        if UserModel.search_from_database_by_username(data["username"]):
            return {"message": "The username has been used"}, 400

        UserModel.add_to_database(UserModel(**data))
        return {"message": "User is successfully created"}, 201


class Profile(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "username",
        type=str,
        required=True,
        help="This field cannot be left blank")
    parser.add_argument(
        "gender",
        type=str,
        required=True,
        help="This field cannot be left blank")
    parser.add_argument(
        "birthday",
        type=str,
        required=True,
        help="This field cannot be left blank")
    parser.add_argument(
        "address",
        type=str,
        required=True,
        help="This field cannot be left blank")
    parser.add_argument(
        "job",
        type=str,
        required=True,
        help="This field cannot be left blank")

    @jwt_required()
    def post(self):
        data = Profile.parser.parse_args()

        user = UserModel.search_from_database_by_username(data["username"])
        user.update_attributes(**data)

        UserModel.update_to_database(user)

        return {"message": "Update profile successfully"}, 200


class TopLender(Resource):
    def get(self):
        lenders = []
        for lender_id, first_name, last_name, gender, \
            birthday, email, username, password, phone, address, \
            job, free_trial_start, free_trial_end, average_star in UserModel.get_top_lender():
            lender = {
                "id": lender_id,
                "first_name": first_name,
                "last_name": last_name,
                "gender": gender,
                "birthday": birthday,
                "email": email,
                "username": username,
                "password": password,
                "phone": phone,
                "address": address,
                "job": job,
                "free_trial_start": free_trial_start,
                "free_trial_end": free_trial_end,
                "average_star": average_star
            }
            lenders.append(lender)
        return {"top_lender": lenders}, 200


class UserList(Resource):
    @jwt_required()
    def get(self):
        return {"users": [user.json() for user in UserModel.get_all_user()]}, 200
