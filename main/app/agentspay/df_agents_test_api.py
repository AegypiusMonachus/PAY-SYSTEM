from app.models.df_agent_rate_dao import DfAgentRate
from app.models.df_trade_dao import DfTradeDao
from app.models import db


def CountAgentsRate():
    res = db.session.query(DfAgentRate).filter()