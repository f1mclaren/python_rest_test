from flask import request
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from models.item import ItemModel


class Item(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help='This field cannot be left blank.'
                        )
    parser.add_argument('store_id',
                        type=int,
                        required=True,
                        help='Every item needs a store ID.'
                        )

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)

        if item:
            return item.json()
        else:
            return {'message': f'The item {name!r} not found.'}, 400

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': f"An item with name '{name}' already exists."}, 400

        data = Item.parser.parse_args()
        data = request.get_json()

        item = ItemModel(None, name, data['price'], data['store_id'])

        try:
            item.save_to_db()
        except:
            return {'message': 'An error occured inserting the item'}, 500

        return item.json(), 201

    def delete(self, name):
        item = ItemModel.find_by_name(name)

        if item is None:
            return {'message': f"An item with name '{name}' does not exist."}, 400

        item.delete_from_db()

        return {'message': f"The item '{name}' has been deleted."}

    def put(self, name):
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)

        if item:    # Update
            item.price = data['price']
        else:       # Insert
            item = ItemModel(None, name, **data)

        item.save_to_db()

        return item.json()


class ItemList(Resource):
    def get(self):
        return {'items': [item.json() for item in ItemModel.query.all()]}
