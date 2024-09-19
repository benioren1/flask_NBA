from db import db

class Player(db.Model):
    __tablename__ = 'players'
    id = db.Column(db.Integer, primary_key=True)
    playername = db.Column(db.String(50), nullable=False)
    team = db.Column(db.String(50), nullable=False)
    position = db.Column(db.String(50), nullable=False)
    seasons = db.relationship('Season', secondary='player_seasons', backref=db.backref('players'))
    points = db.Column(db.Integer, nullable=False)
    games = db.Column(db.Integer, nullable=False)
    twoPercent = db.Column(db.Float, nullable=False)
    threePercent = db.Column(db.Float, nullable=False)
    ATR = db.Column(db.Float, nullable=False)
    PPG_Ratio = db.Column(db.Float, nullable=False)

    def to_dict(self):
        return {
            'playername': self.playername,
            'team': self.team,
            'position': self.position,
            'seasons': [season.to_dict() for season in self.seasons],
            'points': self.points,
            'games': self.games,
            'twoPercent': self.twoPercent,
            'threePercent': self.threePercent,
            'ATR': self.ATR,
            'PPG_Ratio': self.PPG_Ratio
        }