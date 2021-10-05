import sys

from app import app
from db import db


db.init_app(app)


@app.before_first_request
def create_tables():
    sys.stdout.write(app.config['SQLALCHEMY_DATABASE_URI'])
    db.create_all()
