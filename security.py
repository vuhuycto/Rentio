from werkzeug.security import safe_str_cmp
from models.person import UserModel, AdminModel


def authentication(username, password):
    user = UserModel.search_from_database_by_username(username)
    admin = AdminModel.search_from_database_by_username(username)
    if user and safe_str_cmp(user.password, password):
        return user
    elif admin and safe_str_cmp(admin.password, password):
        return admin


def identity(payload):
    user = UserModel.search_from_database_by_id(payload["identity"])
    admin = AdminModel.search_from_database_by_id(payload["identity"])

    if UserModel.search_from_database_by_username(user.username):
        return user
    elif AdminModel.search_from_database_by_username(admin.username):
        return admin
