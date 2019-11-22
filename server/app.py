from flask import Flask
from flask_cors import CORS
import re


import json
from bson.objectid import ObjectId

def newEncoder(o):
    if type(o) == ObjectId:
        return str(o)
    return o.__str__



# mongo connect
import pymongo
from pymongo import MongoClient
client = MongoClient()
db = client.nhl


game_plays_collection = db['game_plays']


app = Flask(__name__)
CORS(app)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/game_plays')
def get_game_plays():
    return game_plays_collection.find()

@app.route('/game_plays/season/<year>')
def get_game_plays_season(year):
    regx = re.compile("^"+year, re.IGNORECASE)
    return json.dumps(list(game_plays_collection.find({'play_id':regx})), default=newEncoder )


if __name__ == '__main__':
    app.run()
