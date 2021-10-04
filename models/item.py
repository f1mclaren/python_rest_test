from __future__ import annotations

from db import db


class ItemModel(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    price = db.Column(db.Float(precision=2))

    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))
    store = db.relationship('StoreModel')

    def __init__(self, _id, name, price, store_id) -> None:
        self.id = _id
        self.name = name
        self.price = price
        self.store_id = store_id

    @classmethod
    def find_by_name(cls, name) -> ItemModel:
        return cls.query.filter_by(name=name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def json(self):
        return {'id': self.id, 'store_id': self.store_id, 'name': self.name, 'price': self.price}
