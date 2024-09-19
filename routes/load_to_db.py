from flask import Flask, request, jsonify, Blueprint
from services.load_players_to_db import add_all_players_to_database



bp_load = Blueprint('load', __name__)

@bp_load.route('/', methods=['GET'])
def load_players_to_db():
    add_all_players_to_database()
    return jsonify({'message': 'All players loaded successfully!'}), 200


