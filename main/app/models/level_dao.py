from . import db


class LevelDao(db.Model):
    __tablename__ = 'tb_config_levels'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    danger = db.Column(db.Integer)
