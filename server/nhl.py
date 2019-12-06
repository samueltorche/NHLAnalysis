import re
def compare_playoff_season(col, season):
    regx = re.compile("^"+season[:4], re.IGNORECASE)
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
              "from": '$game',
              "localField": 'game_id',
              "foreignField": 'game_id',
              "as": 'game'
            } 
        }
    ])
    return(list(res))


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
 