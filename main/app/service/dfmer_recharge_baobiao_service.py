from sqlalchemy import func

from app.common import keep_two_del
from app.models import db
from app.models.df_trade_dao import DfTradeRechargeDao

def test(critern,page=None, per_page=None):
    res = db.session.query(DfTradeRechargeDao.username,
        func.coalesce(func.count(DfTradeRechargeDao.id), 0).label('dds'),
        func.coalesce(func.sum(DfTradeRechargeDao.amount), 0).label('zje')).filter(*critern).group_by(DfTradeRechargeDao.username)

    res = res.paginate(page, per_page, error_out=False)
    return res




