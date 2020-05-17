from . import db


class WithdrawDao(db.Model):
    __tablename__ = 'tb_withdraw'

    id = db.Column(db.Integer, primary_key=True)
    mer_code = db.Column(db.String)
    user_name = db.Column(db.String)
    mer_name = db.Column(db.String)
    order_no = db.Column(db.String)
    bank_id = db.Column(db.String)
    amount = db.Column(db.Numeric, default=0)
    real_amount = db.Column(db.Numeric, default=0)
    action_time = db.Column(db.Integer)
    audit_time = db.Column(db.Integer)
    audit_user = db.Column(db.Integer)
    state = db.Column(db.Integer,default = 1)
    cost_sx = db.Column(db.Numeric, default=0)
    mer_ip = db.Column(db.String)
    remark = db.Column(db.String)
    account = db.Column(db.String)
    name = db.Column(db.String)
    sf_notify = db.Column(db.Integer, default=0)
    wrdraw_amount = db.Column(db.Numeric, default=0)
    paid_amount = db.Column(db.Numeric, default=0)


class BankDao(db.Model):
    __tablename__ = 'tb_config_bank'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    df_id = db.Column(db.Integer)

    def get_bank(self,id):
        df_id = db.session.query(BankDao.df_id).filter(BankDao.id == id).first()
        if df_id is not None:
            df_id = df_id.df_id
        else:
            df_id = None
        return df_id