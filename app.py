import os

from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from db import db
from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList


app = Flask(__name__)
db_url = os.environ.get('DATABASE_URL') ## SI Code - see comment in 119 "SQLAlchemy cant load plugin for postgres"
if db_url: ## uses environemtn database. If not found uses sqlite database for local work. See video/comments 118
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("://", "ql://", 1) 
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'steve'
api = Api(app)

jwt = JWT(app, authenticate, identity) # JWT creates another end point (/auth) which returns a JWT token after running authenticate. 

api.add_resource(Item, '/item/<string:name>') # e.g. http://127.0.0.1.5000/item/GolfBall
api.add_resource(Store, '/store/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(StoreList, '/stores')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    # video says dont import here 
    #from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)