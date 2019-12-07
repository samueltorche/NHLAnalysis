import re
from pymongo import MongoClient
client = MongoClient()
db = client.nhl

game_plays_collection = db['game_plays']
games_collection = db['game']


def compare_playoff_season(plays, games,season):
    regx = re.compile("^"+season[:4], re.IGNORECASE)
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
        }
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
        }
    ])

    json = { "R": list(regular),
             "P": list(playoff)
            }
    '''
    res = col.aggregate([
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
                "play_id": 1,
                "event": 1,
                "home_g" : "$lgame.home_goals",
                "away_goals": "$lgame.away_goals",
                "gameType": "$lgame.type"
            }
        }
    ])'''

    return(json)


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
    seasons_to_eval = ["20102011", "20112012", "20122013", "20132014", "20142015", "20152016", "20162017", "20172018", "20182019"]
    data = []
    for season in seasons_to_eval:
        list_of_games = games_collection.find({"season": season})
        print("loop season")
        nbr_of_fights = 0
        for game in list_of_games:
            print("loop games")
            list_of_plays = game_plays_collection.find({"game_id": game["game_id"]})
            for play in list_of_plays:
                print("loop plays")
                if play["secondaryType"] == "Fighting":
                    nbr_of_fights += 1
        obj = {
            "season": season,
            "fights": nbr_of_fights
        }
        data.append(obj)
    print(data)
    return data
