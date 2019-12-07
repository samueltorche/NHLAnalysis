import re
import json
import os
from pymongo import MongoClient
client = MongoClient()
db = client.nhl

game_plays_collection = db['game_plays']
games_collection = db['game']

seasons_to_eval = [20102011, 20112012, 20122013, 20132014, 20142015, 20152016, 20162017, 20172018, 20182019]
number_of_games_per_season = [1319, 1316, 806, 1323, 1319, 1321, 1317, 1355, 1358]


def compare_playoff_season(plays, games,season):
    regx = re.compile("^"+season[:4], re.IGNORECASE)
    regx2 = re.compile(".", re.IGNORECASE)
    filename = 'compare_' + season +".json"
    if os.path.exists(filename):
        with open(filename) as json_file:
            _json = json.load(json_file)
            return _json

    playoff = games.aggregate([
        {
            "$match":
            {
                "season": int(season),
                "type" : "P"
            }
        },
        {
            "$group":  
            {
                "_id": "season",
                "game_count" : {"$sum": 1 },
                "goals_count": {
                    "$sum": {
                        "$add": ["$away_goals", "$home_goals"]
                    }
                }
            }
        },
        {

            "$project": {
                "_id": 1,
                "game_count": 1,
                "goals_count": 1,
                "avg": { "$divide": ["$goals_count", "$game_count"] }
            } 
        },

         { "$sort" : { "_id" : 1} }
    ])
    regular = games.aggregate([
        {
            "$match":
            {
                "season": int(season),
                "type" : "R"
            }
        },
        {
            "$group":  
            {
                "_id": "season",
                "game_count" : {"$sum": 1 },
                "goals_count": {
                    "$sum": {
                        "$add": ["$away_goals", "$home_goals"]
                    }
                }
            }
        },
        {

            "$project": {
                "_id": 1,
                "game_count": 1,
                "goals_count": 1,
                "avg": { "$divide": ["$goals_count", "$game_count"] }
            } 
        },

         { "$sort" : { "_id" : 1} }
    ])
    playoff_plays = plays.aggregate([
        {
        "$match":
            {
                "play_id": { "$regex": regx} 
            }
        },

        {
            "$lookup": 
            {
              "from": 'game',
              "localField": 'game_id',
              "foreignField": 'game_id',
              "as": 'lgame'
            } 
        },
        {
            "$match":
            {
                "lgame.type": "P"
            }
        },

        {
            "$project":
            {   
                "event": 1,
            }
        },
        {
            "$group":
            {
                "_id": "$event",
                "count" : {"$sum": 1}
            }
        },

         { "$sort" : { "_id" : 1} }
    ])    

    regular_plays = plays.aggregate([
        {
        "$match":
            {
                "play_id": { "$regex": regx} 
            }
        },

        {
            "$lookup": 
            {
              "from": 'game',
              "localField": 'game_id',
              "foreignField": 'game_id',
              "as": 'lgame'
            } 
        },
        {
            "$match":
            {
                "lgame.type": "R"
            }
        },

        {
            "$project":
            {   
                "event": 1,
            }
        },
        {
            "$group":
            {
                "_id": "$event",
                "count" : {"$sum": 1}
            }
        },

         { "$sort" : { "_id" : 1} }
    ])

    playoff_plays_sec = plays.aggregate([
        {
        "$match":
            {
                "secondaryType": {"$regex": regx2},
                "play_id": { "$regex": regx} 
            }
        },

        {
            "$lookup": 
            {
              "from": 'game',
              "localField": 'game_id',
              "foreignField": 'game_id',
              "as": 'lgame'
            } 
        },
        {
            "$match":
            {
                "lgame.type": "P"
            }
        },

        {
            "$project":
            {   
                "event": 1,
                "secondaryType": 1
            }
        },
        {
            "$group":
            {
                "_id": "$secondaryType",
                "count" : {"$sum": 1}
            }
        },

         { "$sort" : { "_id" : 1} }
    ])    

    regular_plays_sec = plays.aggregate([
        {
        "$match":
            {
                "secondaryType": {"$regex": regx2},
                "play_id": { "$regex": regx} 
            }
        },

        {
            "$lookup": 
            {
              "from": 'game',
              "localField": 'game_id',
              "foreignField": 'game_id',
              "as": 'lgame'
            } 
        },
        {
            "$match":
            {
                "lgame.type": "R"
            }
        },

        {
            "$project":
            {   
                "event": 1,
                "secondaryType": 1
            }
        },
        {
            "$group":
            {
                "_id": "$secondaryType",
                "count" : {"$sum": 1}
            }
        },

         { "$sort" : { "_id" : 1} }
    ])    

    _json = { "R": list(regular),
             "P": list(playoff),
             "PP": list(playoff_plays),
             "RP": list(regular_plays),
             "PPSecondary": list(playoff_plays_sec),
             "RPSecondary": list(regular_plays_sec),
            }

    playoff = _json['P']
    playoff_plays = _json['PP']
    playoff_gc = playoff[0]['game_count']
    for el in playoff_plays:
        el['count'] = el['count']/playoff_gc

    playoff_plays_s = _json['PPSecondary']
    for el in playoff_plays_s:
        el['count'] = el['count']/playoff_gc

    regular_plays_s = _json['RPSecondary']
    for el in regular_plays_s:
        el['count'] = el['count']/playoff_gc

    regular = _json['R']
    regular_plays = _json['RP']
    regular_gc = regular[0]['game_count']
    for el in regular_plays:
        el['count'] = el['count']/regular_gc

    with open(filename, 'w') as outfile:
        json.dump(_json, outfile)

    return(_json)


def get_season_goal_average(col):
    res = col.aggregate([

        {
            "$group": 
            {
              "_id": "$season",
              "game_count" : {"$sum": 1 },
              "goals_count": {
                "$sum": {
                  "$add": ["$away_goals", "$home_goals"]
                }
              }
            }
        },

        {

            "$project": {
                "_id": 1,
                "game_count": 1,
                "goals_count": 1,
                "avg": { "$divide": ["$goals_count", "$game_count"] }
            } 
        },

         { "$sort" : { "_id" : 1} }
    ])
    return(list(res))


def get_season_fights_average():
    data = []
    for season in seasons_to_eval:
        list_of_games = games_collection.find({"season": season})
        print("loop season")
        nbr_of_fights = 0
        for game in list_of_games:
            list_of_plays = game_plays_collection.find({"game_id": game["game_id"]})
            for play in list_of_plays:
                if play["secondaryType"] == "Fighting":
                    nbr_of_fights += 1
        obj = {
            "season": season,
            "fights": nbr_of_fights
        }
        data.append(obj)
    print(data)
    return data
