import re
import json
import os
def compare_playoff_season(plays, games,season):
    regx = re.compile("^"+season[:4], re.IGNORECASE)
    filename = 'compare_' + season +".json"
    if os.path.exists(filename):
        with open(filename) as json_file:
            return json.load(json_file)

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
        }
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
        }
    ])

    _json = { "R": list(regular),
             "P": list(playoff),
             "PP": list(playoff_plays),
             "RP": list(regular_plays)
            }

    with open(filename, 'w') as outfile:
        json.dump(_json, outfile)
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
 