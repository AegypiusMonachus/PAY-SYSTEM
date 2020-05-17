from . import db

class NotifyDao(db.Model):
    __tablename__ = 'tb_notify_notice'

    id = db.Column(db.Integer, primary_key=True)
    action_time = db.Column(db.Integer)
    mer_code = db.Column(db.String)
    expansion_data = db.Column(db.JSON)
    success = db.Column(db.Integer)
    status_code = db.Column(db.Integer)
    response = db.Column(db.String)
    order_no = db.Column(db.String)
    
class DfNotifyDao(db.Model):
    __tablename__ = 'tb_df_notify_notice'

    id = db.Column(db.Integer, primary_key=True)
    action_time = db.Column(db.Integer)
    mer_code = db.Column(db.String)
    expansion_data = db.Column(db.JSON)
    success = db.Column(db.Integer)
    status_code = db.Column(db.Integer)
    response = db.Column(db.String)
    order_no = db.Column(db.String)