import os
import datetime

from flask import Flask
from database import database as db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:sesame@localhost:3306/rentio'
app.config['SQLALCHEMY_ECHO'] = True
app.secret_key = os.urandom(16)


@app.route("/")
def index():
    return "Hello World"


if __name__ == '__main__':
    app.run()
