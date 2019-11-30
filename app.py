import os

from flask import Flask
from database import Base, Session, engine

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
# app.config['SQLALCHEMY_ECHO'] = True
app.secret_key = os.urandom(16)

Base.metadata.create_all(engine)


@app.route("/")
def index():
    return str(os.getcwd())


if __name__ == '__main__':
    app.run()

