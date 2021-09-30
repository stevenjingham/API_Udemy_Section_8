from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from models.item import ItemModel

class Item(Resource):
    parser = reqparse.RequestParser() ## Using parser & the way used below, means only price will be updated. Good to avoid mistakes
    parser.add_argument('price', 
        type=float,
        required = True,
        help="This field cannot be left blank"
    )
    parser.add_argument('store_id', 
        type=float,
        required = True,
        help="store_id cannot be left blank"
    )


    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item {} not found'.format(name)}, 404

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': 'An item with name {} already exists'.format(name)}, 400 # 400 is HTTP for bad request. 
        
        data = Item.parser.parse_args()

        item = ItemModel(name, data['price'], data['store_id'])
        
        try:
            item.save_to_db()
        except:
            return {"message":"An error occurred inserting the item."}, 500 #500 is internal server error


        return item.json(), 201 # 201 is code for created. (200 is all OK)  

    def delete(self, name):
        item = ItemModel.find_by_name(name)

        if item:
            item.delete_from_db()
        return {'message': 'Item {} not found, so could not be deleted'.format(name)}, 404
    
    def put(self, name):
        data = Item.parser.parse_args()
        
        # Looks for item. If already exists, update it. If does not exist, insert it
        item = ItemModel.find_by_name(name)
        
        if item is None:
            item = ItemModel(name,data['price'], data['store_id'])
        else:
            item.price = data['price']

        item.save_to_db()
        return item.json()


class ItemList(Resource):
    def get(self):
        ## GET LIST OF ALL ITEMS
        return {'items': [item.json() for item in ItemModel.query.all()]}