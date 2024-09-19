from flask import Flask, request, jsonify,Blueprint
import json
from services.servic_to_load_json import save_to_json
from requests import request
bp_reader = Blueprint('read', __name__)



@bp_reader.route('/', methods=['GET'])
def fetch_player_data():
    years = [2022, 2023, 2024]
    player_data = []

    for year in years:
        url = f"http://b8c40s8.143.198.70.30.sslip.io/api/PlayerDataTotals/query?season={year}&pageSize=1000"
        response = request('GET', url)

        if response.status_code == 200:
            data = response.json()
            player_data.extend(data)
        else:
            print(f"Failed to fetch data for season {year}: {response.status_code}")
    save_to_json(player_data, 'files\\nba_players_data.json')
    return player_data











