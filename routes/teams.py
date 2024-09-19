from flask import Flask, jsonify, request, Blueprint

from models.player import Player
from models.team import Team
from db import db
bp_teams = Blueprint('teams', __name__)




@bp_teams.route('/', methods=['POST'])
def create_team():
    data = request.get_json()
    if 'teamname' not in data or 'playerId' not in data or len(data['playerId']) < 5:
        return jsonify({'error': 'Missing required fields'}), 400
    teamname = data['teamname']
    players_id = data['playerId']
    dict_position = {}
    for player in players_id:
        this_player = Player.query.filter_by(playerId=player).first()

        dict_position[this_player.position] = player
    new_team = Team(teamname=teamname, C=dict_position.get('C', None),
                    PF=dict_position.get('PF', None),
                    SF=dict_position.get('SF', None), SG=dict_position.get('SG', None),
                    PG=dict_position.get('PG', None) )
    db.session.add(new_team)
    db.session.commit()

    return jsonify(new_team.to_dict()), 201