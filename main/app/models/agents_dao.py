from . import db


class Agents(db.Model):
    __tablename__ = 'tb_agents'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    rate = db.Column(db.String)
    type = db.Column(db.Integer)
    level = db.Column(db.Integer)
    mobilephone = db.Column(db.String)
    email = db.Column(db.String)
    name = db.Column(db.String)
    remark = db.Column(db.String)
    count = db.Column(db.Integer)
    greattime = db.Column(db.Integer)
    parent_code = db.Column(db.Integer)
    secret_key = db.Column(db.String)
    amount = db.Column(db.Numeric)
    default_level = db.Column(db.Integer)
    mer_code = db.Column(db.String)
    state = db.Column(db.Integer)
    is_delete = db.Column(db.Integer, default=0)
