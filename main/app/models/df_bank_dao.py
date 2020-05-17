from . import db


class DfBanks(db.Model):
    __tablename__ = 'tb_df_bank'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column('bank_name',db.String)
    bank_number = db.Column(db.String)
    bank_code = db.Column(db.String)
    bank_id = db.Column(db.Integer)
    default_bank = db.Column(db.Integer)

class DfBanksAndMer(db.Model):
    __tablename__ = 'tb_df_merchant_bank'

    id = db.Column(db.Integer, primary_key=True)
    mer_code = db.Column(db.String)
    df_bank_id = db.Column(db.Integer)