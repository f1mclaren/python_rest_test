from __future__ import annotations

from db import db


class StoreModel(db.Model):
    __tablename__ = 'stores'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))

    items = db.relationship('ItemModel', lazy='dynamic')

    def __init__(self, _id, name) -> None:
        self.id = _id
        self.name = name

    @classmethod
    def find_by_name(cls, name) -> StoreModel:
        return cls.query.filter_by(name=name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def json(self):
        return {'id': self.id, 'name': self.name, 'items': [item.json() for item in self.items.all()]}
