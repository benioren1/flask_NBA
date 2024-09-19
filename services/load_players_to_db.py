import json
from itertools import groupby

from flask import session

from db import db
from models.player import Player
from services.servic_to_load_json import save_to_json, load_json

#פונקציה שמסדרת לי את הגייסון ממויין לצורך ביצוע פעולות
def sorrted_json_by_name():
    players = json.load(open('..\\files\\nba_players_data.json'))
    sorted_players = sorted(players, key=lambda x: x['playerName'])
    transaction_by_type = {}
    for key, group in groupby(sorted_players, key=lambda x: x['playerName']):
        transaction_by_type[key] = [x for x in list(group)]
    save_to_json(transaction_by_type, '..\\files\\nba_players_data.json')
    return transaction_by_type

#פונקציה שיוצרת שחקן אחד כל פעם
def create_player_to_object(player):
    avg_points = get_avg_points_per_season(player['position'])

    if player['games'] != 0 and avg_points != 0:
        PPG_Ratio = (player['points'] / player['games']) / avg_points
    else:
        PPG_Ratio = 0

    return Player(
        playerId=player['playerId'],
        playerName=player['playerName'],
        team=player['team'],
        position=player['position'],
        season=player['season'],
        points=player['points'],
        games=player['games'],
        twoPercent=player['twoPercent'],
        threePercent=player['threePercent'],
        ATR=(player['assists'] / player['turnovers'] if player['turnovers'] != 0 else 0),
        PPG_Ratio=PPG_Ratio
    )


#פונקציה שמכניסה את כל השחקנים לדאטה
def add_all_players_to_database():
    all_players = load_json('files/nba_players_data.json')
    for player in all_players:
        new_player = create_player_to_object(player)
        db.session.add(new_player)
        db.session.commit()
    return 'All players added to the database.'

#פונקציה שמחשבת ממוצע עונתי לכל עמדה
def get_avg_points_per_season(position):
    players = Player.query.filter_by(position=position).all()
    total_points = sum(player.points for player in players)
    total_games = sum(player.games for player in players)
    return total_points / total_games if total_games!= 0 else 0
