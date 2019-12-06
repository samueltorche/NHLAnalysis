import re
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
 