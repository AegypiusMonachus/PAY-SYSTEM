from . import db


class UserDao(db.Model):
    __tablename__ = 'tb_sys_user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    password = db.Column(db.String)