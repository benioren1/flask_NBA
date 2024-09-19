from enum import unique

from db import db

class Team(db.Model):
    __tablename__ = 'teams'
    id = db.Column(db.Integer, primary_key=True)
    teamname = db.Column(db.String(50), nullable=False)
    C = db.Column(db.String(50),unique=True, nullable=True)
    PF = db.Column(db.String(50),unique=True, nullable=True)
    SF = db.Column(db.String(50),unique=True, nullable=True)
    SG = db.Column(db.String(50),unique=True, nullable=True)
    PG = db.Column(db.String(50),unique=True, nullable=True)


    def to_dict(self):
        return {"teamname": self.teamname, "C": self.C, "PF": self.PF, "SF": self.SF, "SG": self.SG, "PG": self.PG}