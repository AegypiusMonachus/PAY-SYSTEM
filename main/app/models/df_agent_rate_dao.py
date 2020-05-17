from . import db


class DfAgentRate(db.Model):
    __tablename__ = 'tb_df_agents_rate'

    id = db.Column(db.Integer, primary_key=True)
    agent_code = db.Column(db.String)
    agent_name = db.Column(db.String)
    mer_code = db.Column(db.String)
    rate_prop = db.Column(db.Numeric)
    rate_amount = db.Column(db.JSON)
    mer_username = db.Column(db.String)


class SelfAgentRate(db.Model):
    __tablename__ = 'tb_df_agents_rate_self'

    id = db.Column(db.Integer, primary_key=True)
    agent_code = db.Column(db.String)
    agent_name = db.Column(db.String)
    rate_prop = db.Column(db.Numeric, default=0)
    rate_amount = db.Column(db.JSON)
