from flask import Flask, jsonify, request, Blueprint

from models.player import Player
from models.team import Team
from db import db
bp_teams = Blueprint('teams', __name__)



#יצירת קבוצה של שחקנים
@bp_teams.route('/', methods=['POST'])
def create_team():
    data = request.get_json()
    min_players = 5
    if 'teamname' not in data or 'playerId' not in data or len(data['playerId']) < min_players:
        return jsonify({'error': 'Missing required fields'}), 400
    teamname = data['teamname']
    players_id = data['playerId']
    dict_position = {}
    for player in players_id:
        this_player = Player.query.filter_by(playerId=player).first()

        dict_position[this_player.position] = player
    if len(dict_position) < min_players:
        return jsonify({'error': 'Missing required fields'}), 400
    new_team = Team(teamname=teamname, C=dict_position['C'],
                    PF=dict_position['PF'],
                    SF=dict_position['SF'],
                    SG=dict_position['SG'],
                    PG=dict_position['PG'])

    db.session.add(new_team)
    db.session.commit()

    return jsonify(new_team.to_dict()), 201

@bp_teams.route('/<int:team_id>', methods=['PUT'])
def update_team(team_id):
    team = Team.query.get_or_404(team_id)
    print(team.to_dict())
    data = request.get_json()
    min_players = 5
    players_id = data['playerId']
    dict_position = {}
    for player in players_id:
        this_player = Player.query.filter_by(playerId=player).first()

        dict_position[this_player.position] = player
    if len(dict_position) < min_players:
        return jsonify({'error': 'Missing required fields'}), 400

    team.teamname = data['teamname'] if 'teamname' in data else team.teamname
    team.C=dict_position['C']
    team.PF=dict_position['PF']
    team.SF=dict_position['SF']
    team.SG=dict_position['SG']
    team.PG=dict_position['PG']
    db.session.commit()
    return jsonify(team.to_dict()), 200