from . import db


class RefulationDao(db.Model):
    __tablename__ = 'tb_config_regulation'

    id = db.Column(db.Integer, primary_key=True)
    lower_amount = db.Column(db.Numeric, default=0)
    upper_amount = db.Column(db.Numeric, default=0)
    agents = db.Column(db.String)
    increase_base = db.Column(db.Integer)
    reduce_base = db.Column(db.Integer)
    stop_service = db.Column('stop_service_base',db.Integer)
    efficiency = db.Column(db.JSON)
    exempt = db.Column(db.Integer)
    notify_times = db.Column('retransmission_times',db.Integer)
    pay_times = db.Column('pay_expires_time',db.Integer)
    pay_url_times  = db.Column('pay_url_expires_time',db.Integer)
    perday_income = db.Column(db.Numeric, default=0)
    repetition_time = db.Column(db.Integer)
    small_limit_lower = db.Column(db.Numeric)#小额区间下限
    small_limit_upper = db.Column(db.Numeric)#小额区间上限
    large_limit_lower = db.Column(db.Numeric)#大额区间下限
    large_limit_upper = db.Column(db.Numeric)#大额区间上线
