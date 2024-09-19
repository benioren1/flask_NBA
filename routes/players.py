from flask import Flask, jsonify, request,Blueprint
from db import db
from models.player import Player

bp_players= Blueprint('players', __name__)


#פונקציה שמחזירה שחקנים לפי עמדה שלהם ושנה
@bp_players.route('/', methods=['GET'])
def get_players_by_position():
    position = request.args.get('position')
    season = request.args.get('season')
    if not season:
        all_players = db.session.query(Player).filter_by(position=position).all()
        return jsonify([player.to_dict() for player in all_players])

    all_players = db.session.query(Player).filter_by(position=position, season=season).all()
    return jsonify([player.to_dict() for player in all_players])

