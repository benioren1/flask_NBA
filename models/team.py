from db import db

class Team(db.Model):
    __tablename__ = 'teams'
    id = db.Column(db.Integer, primary_key=True)
    teamname = db.Column(db.String(50), nullable=False)
    players_id = db.relationship('Player', backref='team', lazy='dynamic')


    def to_dict(self):
        return {"id": self.id, "teamname": self.teamname, "players": [player.to_dict() for player in self.players_id]}