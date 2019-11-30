import os

from flask import Flask
from flask_restful import Api
from database import Base, Session, engine

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
# app.config['SQLALCHEMY_ECHO'] = True
app.secret_key = os.urandom(16)


@app.route("/")
def index():
    return "Hello World"


api = Api(app)

Base.metadata.create_all(engine)

if __name__ == '__main__':
    app.run()

