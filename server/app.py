from flask import Flask
from flask_cors import CORS
import re
import nhl


import json
from bson.objectid import ObjectId

def newEncoder(o):
    if type(o) == ObjectId:
        return str(o)
    if isinstance(o, ObjectId):
            return str(o)
    return o.__str__



# mongo connect
import pymongo
from pymongo import MongoClient
client = MongoClient()
db = client.nhl



game_plays_collection = db['game_plays']
games_collection = db['game']


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


@app.route('/game_plays/games/<game_id>')
def get_game_match(game_id):
    return json.dumps(list(game_plays_collection.find({'game_id':int(game_id)})), default=newEncoder )


@app.route('/season/avg_goal')
def get_season_avg_goal():
    data = nhl.get_season_goal_average(games_collection)
    return json.dumps(data)


@app.route('/season/avg_shots')
def get_season_avg_shots():
    data = nhl.get_avg_nbr_shots()
    return json.dumps(data)


@app.route('/season/avg_fights')
def get_season_avg_fights():
    data = nhl.get_season_fights_average()
    return json.dumps(data)


@app.route('/season/avg_penalties')
def get_season_avg_penalties():
    data = nhl.get_season_penalties_average()
    return json.dumps(data)


@app.route('/games_plays/compare/<season>')
def get_compare_playoff_season(season):
    data = nhl.compare_playoff_season(game_plays_collection, games_collection,season)
    return json.dumps(data)


@app.route('/player_stats')
def get_players_stats():
    data = nhl.get_player_details()
    return json.dumps(data)


if __name__ == '__main__':
    app.run(debug=True,host= '0.0.0.0')
    # app.run(debug=True)













