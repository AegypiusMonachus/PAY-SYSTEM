from . import db

class DFRechargeBankDAO(db.Model):
    __tablename__ = 'tb_df_recharge_bank'

    id = db.Column(db.Integer, primary_key=True)
    bank_id = db.Column(db.Integer)
    account = db.Column(db.String)
    name = db.Column(db.String)
    