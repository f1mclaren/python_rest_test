import sys

from app import app
from db import db

sys.stdout.write(get_db_url())

db.init_app(app)


@app.before_first_request
def create_tables():
    db.create_all()
