from flask import request
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from models.store import StoreModel


class Store(Resource):

    parser = reqparse.RequestParser()

    @jwt_required()
    def get(self, name):
        store = StoreModel.find_by_name(name)

        if store:
            return store.json()
        else:
            return {'message': f'The store {name!r} not found.'}, 400

    def post(self, name):
        if StoreModel.find_by_name(name):
            return {'message': f"A store with name '{name}' already exists."}, 400

        data = Store.parser.parse_args()
        data = request.get_json()

        store = StoreModel(None, name)

        try:
            store.save_to_db()
        except:
            return {'message': 'An error occured inserting the store'}, 500

        return store.json(), 201

    def delete(self, name):
        store = StoreModel.find_by_name(name)

        if store is None:
            return {'message': f"A store with name '{name}' does not exist."}, 400

        store.delete_from_db()

        return {'message': f"The store '{name}' has been deleted."}


class StoreList(Resource):
    def get(self):
        return {'stores': [store.json() for store in StoreModel.query.all()]}
