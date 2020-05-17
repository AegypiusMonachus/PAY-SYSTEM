from . import db

'''人工匹配--额度确认'''
class OnlineTradeConfirmDao(db.Model):
    __tablename__ = 'tb_onlinetrade_confirm'

    id = db.Column(db.Integer, primary_key=True)
    order_no = db.Column(db.String)
    bank_order_no = db.Column(db.String)
    amount = db.Column(db.Numeric, default=0)
    qr_code = db.Column(db.String)
    audit_time = db.Column(db.Integer)
    cost_service = db.Column(db.Numeric, default=0)
    cost_agent = db.Column(db.Numeric, default=0)
    administrator = db.Column(db.String)
    mer_code = db.Column(db.String)



