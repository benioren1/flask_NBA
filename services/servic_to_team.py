from flask import jsonify

from models.player import Player
from models.team import Team

#מקבלת מזהה ומחזירה לי בסוף את כל הppg של הקבוצה הזאת פונקציה ש
def get_team1(team_id):
    team = Team.query.get_or_404(team_id)
    my_list = [team.C, team.PF, team.SF, team.SG, team.PG]
    dict_team = {}
    for player_id in my_list:
        player = Player.query.filter_by(playerId=player_id).first()
        dict_team[player.position] = player.to_dict()

    sum_ppg = sum_PPG(dict_team)
    return sum_ppg


def sum_PPG(my_dict):
    total = 0
    for player in my_dict.values():
        total += player['PPG_Ratio']
    return total