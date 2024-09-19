from flask import Flask, jsonify, request, Blueprint

from models.player import Player
from models.team import Team
from db import db
from services.servic_to_team import get_team1

bp_teams = Blueprint('teams', __name__)

#מקבל את הנתונים של הקבוצה ובודק תקינות יוצר ומחזיר לפונקציה להכניס לdb
def create(data):
    teamname = data['teamname']
    players_id = data['playerId']
    dict_position = {}
    min_players = 5
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
    return new_team

#יצירת קבוצה של שחקנים
@bp_teams.route('/', methods=['POST'])
def create_team():
    data = request.get_json()
    min_players = 5
    if 'teamname' not in data or 'playerId' not in data or len(data['playerId']) < min_players:
        return jsonify({'error': 'Missing required fields'}), 400
    try:
        new_team = create(data)
        db.session.add(new_team)
        db.session.commit()
        return jsonify(new_team.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': "your have a problem in your requests"}), 400




#פןנקציה שמעדכנת קבוצה
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

#פונקציה שמוחקת קבוצה
@bp_teams.route('/<int:team_id>', methods=['DELETE'])
def delete_team(team_id):
    team = Team.query.get_or_404(team_id)
    db.session.delete(team)
    db.session.commit()
    return jsonify({'message': 'team deleted'}), 200


#פונקציה למחיקה להצגה של קבוצה
@bp_teams.route('/<int:team_id>', methods=['GET'])
def get_team(team_id):
    team = Team.query.get_or_404(team_id)
    my_list = [team.C , team.PF, team.SF, team.SG, team.PG ]
    dict_team = {}
    for i in range(len(my_list)):
        player = Player.query.filter_by(playerId=my_list[i]).first()
        dict_team[player.position] = player.to_dict()
    return jsonify({'name':team.teamname,'players': dict_team}), 200

@bp_teams.route('/compare', methods=['GET'])
def equal_between_teams():
    team1_id = request.args.get('team1')
    team2_id = request.args.get('team2')
    print(team1_id, team2_id)
    team1_ppg = get_team1(team1_id)
    team2_ppg = get_team1(team2_id)
    print(team1_ppg, team2_ppg)

    if team1_ppg > team2_ppg:
        return jsonify({'message': 'Team 1 is bigger'}), 200
    elif team1_ppg < team2_ppg:
        return jsonify({'message': 'Team 2 is bigger'}), 200
    else:
        return jsonify({'message': 'Both teams are equal'}), 200



