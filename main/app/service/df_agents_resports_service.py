from app.models.df_trade_dao import DfTradeSxfDao,DfTradeDao
from app.models import db
from sqlalchemy import func
from app.models.merchant_dao import MerchantDao
from app.models.df_agent_rate_dao import DfAgentRate


class DfAgentsResportsSer():
    def __init__(self):
        pass


    def get_kk(self,critern = None,critern_xinyong = None,critern_sxf = None,page=None,per_page=None):
        res_one = db.session.query(
            DfTradeDao.mer_username.label('username'),
            func.count(DfTradeDao.id).label('number'),
            func.sum(DfTradeDao.amount).label('amount')
        ).filter(DfTradeDao.state==2).filter(*critern_xinyong).group_by(DfTradeDao.mer_username)
        res_one = res_one.subquery()

        res_sum = db.session.query(
            DfAgentRate.agent_name.label('agent_name'),
            func.coalesce(func.sum(res_one.c.number),0).label('number'),
            func.coalesce(func.sum(res_one.c.amount),0).label('amount')
        ).filter(*critern).group_by(DfAgentRate.agent_name)
        res_sum = res_sum.outerjoin(res_one,res_one.c.username == DfAgentRate.mer_username)
        res_sum = res_sum.subquery()



        res_sxf = db.session.query(
            DfTradeSxfDao.agents_username.label('agent_name'),
            func.coalesce(func.sum(DfTradeSxfDao.sxf),0).label('sxf')
        ).filter(*critern_sxf).group_by(DfTradeSxfDao.agents_username)
        res_sxf = res_sxf.subquery()

        res = db.session.query(
            res_sum.c.agent_name.label('agent_name'),
            res_sum.c.number.label('number'),
            res_sum.c.amount.label('amount'),
            res_sxf.c.sxf.label('sxf')
        )
        res = res.outerjoin(res_sxf, res_sxf.c.agent_name == res_sum.c.agent_name)
        res = res.paginate(page, per_page, error_out=False)
        return res



    def get_merchart(self,critern = None,critern_xinyong = None,critern_sxf = None,page=None,per_page=None):
        res_one = db.session.query(
            DfTradeDao.mer_username.label('username'),
            func.count(DfTradeDao.id).label('number'),
            func.sum(DfTradeDao.amount).label('amount')
        ).filter(DfTradeDao.state == 2).filter(*critern_xinyong).group_by(DfTradeDao.mer_username)
        res_one = res_one.subquery()

        res_sum = db.session.query(
            DfAgentRate.agent_name.label('agent_name'),
            func.coalesce(func.sum(res_one.c.number), 0).label('number'),
            func.coalesce(func.sum(res_one.c.amount), 0).label('amount')
        ).filter(*critern).group_by(DfAgentRate.agent_name)
        res_sum = res_sum.outerjoin(res_one, res_one.c.username == DfAgentRate.mer_username)
        res_sum = res_sum.subquery()

        res_sxf = db.session.query(
            DfTradeSxfDao.agents_username.label('agent_name'),
            func.coalesce(func.sum(DfTradeSxfDao.sxf), 0).label('sxf')
        ).filter(*critern_sxf).group_by(DfTradeSxfDao.agents_username)
        res_sxf = res_sxf.subquery()

        res = db.session.query(
            res_sum.c.agent_name.label('agent_name'),
            res_sum.c.number.label('number'),
            res_sum.c.amount.label('amount'),
            res_sxf.c.sxf.label('sxf')
        )
        res = res.outerjoin(res_sxf, res_sxf.c.agent_name == res_sum.c.agent_name)
        res = res.paginate(page, per_page, error_out=False)
        return res