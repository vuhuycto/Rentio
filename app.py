import os
import datetime

from flask import Flask
from database import database as db
from models.user import UserModel
from models.admin import AdminModel

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:sesame@localhost:3306/rentio'
app.config['SQLALCHEMY_ECHO'] = True
app.secret_key = os.urandom(16)


def main():
    db.init_app(app)
    db.create_all()


if __name__ == '__main__':
    with app.app_context():
        main()
