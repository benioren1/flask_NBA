from flask import Flask
from db import db
from routes.read_api import bp_reader
from routes.load_to_db import bp_load
from routes.players import bp_players

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///NBA.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


with app.app_context():

    db.create_all()


app.register_blueprint(bp_reader, url_prefix='/api/reader')
app.register_blueprint(bp_load, url_prefix='/api/load')
app.register_blueprint(bp_players, url_prefix='/api/players')




if __name__ == '__main__':
    app.run(debug=True)
