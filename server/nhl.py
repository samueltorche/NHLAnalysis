import re
import json
import os
from pymongo import MongoClient

client = MongoClient()
db = client.nhl

game_plays_collection = db['game_plays']
games_collection = db['game']
skater_collection = db['shifts']
players_collection = db['players']

seasons_to_eval = [20102011, 20112012, 20122013, 20132014, 20142015, 20152016, 20162017, 20172018, 20182019]
number_of_games_per_season = [1319, 1316, 806, 1323, 1319, 1321, 1317, 1355, 1358]


def compare_playoff_season(plays, games, season):
    regx = re.compile("^" + season[:4], re.IGNORECASE)
    regx2 = re.compile(".", re.IGNORECASE)
    filename = 'compare_' + season + ".json"
    if os.path.exists(filename):
        with open(filename) as json_file:
            _json = json.load(json_file)
            return _json

    playoff = games.aggregate([
        {
            "$match":
                {
                    "season": int(season),
                    "type": "P"
                }
        },
        {
            "$group":
                {
                    "_id": "season",
                    "game_count": {"$sum": 1},
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
                "avg": {"$divide": ["$goals_count", "$game_count"]}
            }
        },

        {"$sort": {"_id": 1}}
    ])
    regular = games.aggregate([
        {
            "$match":
                {
                    "season": int(season),
                    "type": "R"
                }
        },
        {
            "$group":
                {
                    "_id": "season",
                    "game_count": {"$sum": 1},
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
                "avg": {"$divide": ["$goals_count", "$game_count"]}
            }
        },

        {"$sort": {"_id": 1}}
    ])
    playoff_plays = plays.aggregate([
        {
            "$match":
                {
                    "play_id": {"$regex": regx}
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
                    "count": {"$sum": 1}
                }
        },

        {"$sort": {"_id": 1}}
    ])

    regular_plays = plays.aggregate([
        {
            "$match":
                {
                    "play_id": {"$regex": regx}
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
                    "count": {"$sum": 1}
                }
        },

        {"$sort": {"_id": 1}}
    ])

    playoff_plays_sec = plays.aggregate([
        {
            "$match":
                {
                    "secondaryType": {"$regex": regx2},
                    "play_id": {"$regex": regx}
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
                    "count": {"$sum": 1}
                }
        },

        {"$sort": {"_id": 1}}
    ])

    regular_plays_sec = plays.aggregate([
        {
            "$match":
                {
                    "secondaryType": {"$regex": regx2},
                    "play_id": {"$regex": regx}
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
                    "count": {"$sum": 1}
                }
        },

        {"$sort": {"_id": 1}}
    ])

    _json = {"R": list(regular),
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
        el['count'] = el['count'] / playoff_gc

    playoff_plays_s = _json['PPSecondary']
    for el in playoff_plays_s:
        el['count'] = el['count'] / playoff_gc

    regular_plays_s = _json['RPSecondary']
    for el in regular_plays_s:
        el['count'] = el['count'] / playoff_gc

    regular = _json['R']
    regular_plays = _json['RP']
    regular_gc = regular[0]['game_count']
    for el in regular_plays:
        el['count'] = el['count'] / regular_gc

    with open(filename, 'w') as outfile:
        json.dump(_json, outfile)

    return (_json)


def get_season_goal_average(col):
    res = col.aggregate([

        {
            "$group":
                {
                    "_id": "$season",
                    "game_count": {"$sum": 1},
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
                "avg": {"$divide": ["$goals_count", "$game_count"]}
            }
        },

        {"$sort": {"_id": 1}}
    ])
    return (list(res))


def get_season_fights_average():
    '''
    data = []
    for season in seasons_to_eval:
        list_of_games = games_collection.find({"season": season})
        nbr_of_fights = 0
        for game in list_of_games:
            fights = game_plays_collection.find({"game_id": game["game_id"], "secondaryType": "Fighting"}).count()
            nbr_of_fights += fights
        obj = {
            "season": season,
            "fights": nbr_of_fights
        }
        data.append(obj)
    print(data)
    '''
    data = [{'season': 20102011, 'fights': 1286}, {'season': 20112012, 'fights': 1102},
            {'season': 20122013, 'fights': 703}, {'season': 20132014, 'fights': 934},
            {'season': 20142015, 'fights': 785}, {'season': 20152016, 'fights': 674},
            {'season': 20162017, 'fights': 756},
            {'season': 20172018, 'fights': 558}, {'season': 20182019, 'fights': 456}]
    i = 0
    for obj in data:
        obj['fights_avg'] = obj['fights'] / number_of_games_per_season[i]
        i += 1
    return data


def get_season_penalties_average():
    '''
    data = []
    for season in seasons_to_eval:
        list_of_games = games_collection.find({"season": season})
        nbr_of_penalties = 0
        for game in list_of_games:
            penalties = game_plays_collection.find({"game_id": game["game_id"], "event": "Penalty"}).count()
            nbr_of_penalties += penalties
        obj = {
            "season": season,
            "penalties": nbr_of_penalties
        }
        data.append(obj)
    i = 0
    for obj in data:
        obj['penalties_avg'] = obj['penalties'] / number_of_games_per_season[i]
        i += 1
    print(data)
    '''
    data = [{'season': 20102011, 'penalties': 12253, 'penalties_avg': 9.289613343442001},
            {'season': 20112012, 'penalties': 11492, 'penalties_avg': 8.732522796352583},
            {'season': 20122013, 'penalties': 7115, 'penalties_avg': 8.827543424317618},
            {'season': 20132014, 'penalties': 11386, 'penalties_avg': 8.606198034769463},
            {'season': 20142015, 'penalties': 10351, 'penalties_avg': 7.847611827141774},
            {'season': 20152016, 'penalties': 10444, 'penalties_avg': 7.906131718395155},
            {'season': 20162017, 'penalties': 10052, 'penalties_avg': 7.6324981017463935},
            {'season': 20172018, 'penalties': 9948, 'penalties_avg': 7.34169741697417},
            {'season': 20182019, 'penalties': 9704, 'penalties_avg': 7.1458026509572905}]
    return data


def get_avg_nbr_shots():
    '''
    data = []
    for season in seasons_to_eval:
        list_of_games = games_collection.find({"season": season})
        nbr_of_shots = 0
        for game in list_of_games:
            blocked_shots = game_plays_collection.find({"game_id": game["game_id"], "event": "Blocked Shot"}).count()
            missed_shots = game_plays_collection.find({"game_id": game["game_id"], "event": "Missed Shot"}).count()
            shots = game_plays_collection.find({"game_id": game["game_id"], "event": "Shot"}).count()
            goal = game_plays_collection.find({"game_id": game["game_id"], "event": "Goal"}).count()
            nbr_of_shots += blocked_shots
            nbr_of_shots += missed_shots
            nbr_of_shots += shots
            nbr_of_shots += goal
        obj = {
            "season": season,
            "shots": nbr_of_shots
        }
        data.append(obj)
    i = 0
    for obj in data:
        obj['shots_avg'] = obj['shots'] / number_of_games_per_season[i]
        i += 1
    print(data)
    '''
    data = [{'season': 20102011, 'shots': 147186, 'shots_avg': 111.5890826383624},
            {'season': 20112012, 'shots': 144914, 'shots_avg': 110.11702127659575},
            {'season': 20122013, 'shots': 88844, 'shots_avg': 110.22828784119106},
            {'season': 20132014, 'shots': 147455, 'shots_avg': 111.45502645502646},
            {'season': 20142015, 'shots': 146864, 'shots_avg': 111.34495830174374},
            {'season': 20152016, 'shots': 144388, 'shots_avg': 109.30204390613171},
            {'season': 20162017, 'shots': 147700, 'shots_avg': 112.14882308276385},
            {'season': 20172018, 'shots': 157169, 'shots_avg': 115.99188191881919},
            {'season': 20182019, 'shots': 157365, 'shots_avg': 115.879970544919}]
    return data


def get_avg_nbr_hits():
    '''
    data = []
    for season in seasons_to_eval:
        list_of_games = games_collection.find({"season": season})
        nbr_of_hits = 0
        for game in list_of_games:
            hits = game_plays_collection.find({"game_id": game["game_id"], "event": "Hit"}).count()
            nbr_of_hits += hits
        obj = {
            "season": season,
            "hits": nbr_of_hits
        }
        data.append(obj)
    i = 0
    for obj in data:
        obj['hits_avg'] = obj['hits'] / number_of_games_per_season[i]
        i += 1
    print(data)
    '''
    data = [{'season': 20102011, 'hits': 59857, 'hits_avg': 45.380591357088704},
            {'season': 20112012, 'hits': 60519, 'hits_avg': 45.9870820668693},
            {'season': 20122013, 'hits': 39794, 'hits_avg': 49.37220843672456},
            {'season': 20132014, 'hits': 62973, 'hits_avg': 47.59863945578231},
            {'season': 20142015, 'hits': 66342, 'hits_avg': 50.297194844579224},
            {'season': 20152016, 'hits': 61615, 'hits_avg': 46.64269492808479},
            {'season': 20162017, 'hits': 58635, 'hits_avg': 44.521640091116176},
            {'season': 20172018, 'hits': 58962, 'hits_avg': 43.51439114391144},
            {'season': 20182019, 'hits': 62576, 'hits_avg': 46.079528718703976}]
    return data


def get_player_details():
    filename = 'player_stats.json'
    if os.path.exists(filename):
        with open(filename) as json_file:
            _json = json.load(json_file)
            return _json

    best_players = [8471214, 8474564, 8474141, 8475166, 8470794]
    seasons = [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018]
    res = {}
    for season in seasons:
        res[season] = {}
        for bp in best_players:
            regx = re.compile("^" + str(season), re.IGNORECASE)
            stats = skater_collection.aggregate([
                {
                    "$project":
                        {
                            "game_id": {"$toLower": "$game_id"},
                            "goals": 1,
                            "timeOnIce": 1,
                            "player_id": 1
                        }
                },
                {
                    "$match":
                        {
                            "game_id": {"$regex": regx},
                            "player_id": bp
                        }
                },

                {
                    "$group":
                        {
                            "_id": "$player_id",
                            "goals": {"$sum": "$goals"},
                            "timeOnIce": {"$sum": "$timeOnIce"}
                        }
                },
                {
                    "$sort":
                        {
                            "goals": -1,
                            "_id": 1
                        }
                }
            ])

            _players = list(stats)
            for _player in _players:
                pid = _player['_id']
                player = list(players_collection.find({'player_id': pid}))[0]
                _player['_id'] = player['lastName'] + " " + player['firstName']
                # _player['_id'] = 10

            res[season][bp] = _players

    with open(filename, 'w') as outfile:
        json.dump(res, outfile)
    return res


def get_playoff(season):
    filename = "playoff_" + str(season) + ".json"
    with open(filename) as json_file:
        _json = json.load(json_file)
        return _json
