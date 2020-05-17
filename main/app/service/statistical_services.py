from app.models.onlinetrades_dao import OnlinetradesDao
from app.models.withdraw_dao import WithdrawDao
from app.models.merchant_dao import MerchantDao
from app.models.onlinetrade_confirm import OnlineTradeConfirmDao
from app.api_0_1.common import make_response
from app.models import db
from sqlalchemy import and_,func
from app.models.df_trade_dao import DfTradeDao,DfTradeRechargeDao,DfTradeSxfDao
from app.models.refulation_dao import RefulationDao
from sqlalchemy import literal


class StaticSer():
    def __init__(self):
        pass


    def get_date(self,critern=None,critern_jiaoyi = None,critern_tx = None,critern_xinyong = None,critern_df = None,critern_sxf = None):

        df_xinyong = db.session.query(
            literal('9518').label('name'),
            func.count(DfTradeRechargeDao.id).label('xinyong_num'),
            func.coalesce(func.sum(DfTradeRechargeDao.amount),0).label('xinyong_amount')
        ).filter(
            *critern_xinyong
        )


        df_xinyong = df_xinyong.subquery()


        df_jiaoyi = db.session.query(
            literal('9518').label('name'),
            func.count(DfTradeDao.id).label('dfjiaoyi_num'),
            func.coalesce(func.sum(DfTradeDao.amount),0).label('dfjiaoyi_amount')
        ).filter(
            *critern_df
        )


        df_jiaoyi = df_jiaoyi.subquery()

        jiaoyi_qx = db.session.query(
            literal('9518').label('name'),
            func.count(WithdrawDao.id).label('wraw_num'),
            func.coalesce(func.sum(WithdrawDao.amount),0).label('wraw_amount'),
            func.coalesce(func.sum(WithdrawDao.wrdraw_amount),0).label('wrdraw_amount_sxf')
        ).filter(
            *critern
        ).filter(
            *critern_tx
        )
        jiaoyi_qx = jiaoyi_qx.outerjoin(MerchantDao, MerchantDao.code == WithdrawDao.mer_code)

        jiaoyi_qx = jiaoyi_qx.subquery()

        jiaoyi_jy = db.session.query(
            literal('9518').label('name'),
            func.count(OnlinetradesDao.id).label('jiaoyi_num'),
            func.coalesce(func.sum(OnlinetradesDao.amount),0).label('jiaoyi_amount'),
            func.coalesce(func.sum(OnlinetradesDao.real_cost_service),0).label('jiaoyi_amount_service'),
            func.coalesce(func.sum(OnlinetradesDao.real_cost_agent),0).label('jiaoyi_amount_agents'),
        ).filter(
            *critern
        ).filter(
            *critern_jiaoyi
        )
        jiaoyi_jy = jiaoyi_jy.outerjoin(MerchantDao, MerchantDao.code == OnlinetradesDao.mer_code)

        jiaoyi_jy = jiaoyi_jy.subquery()

        df_jiaoyi_order = db.session.query(
            DfTradeDao.order_no
        ).filter(
            *critern_df
        ).all()
        result = []
        for order in df_jiaoyi_order:
            if order is not None:
                result.append(order.order_no)
        df_agents_sxf = db.session.query(
            literal('9518').label('name'),
            func.coalesce(func.sum(DfTradeSxfDao.sxf),0).label('df_sxf')
        ).filter(
            *critern_sxf
        ).filter(DfTradeSxfDao.order_no.in_(result))

        df_agents_sxf = df_agents_sxf.subquery()


        res = db.session.query(
            df_xinyong.c.name.label('name'),
            df_xinyong.c.xinyong_num.label('xinyong_num'),
            df_xinyong.c.xinyong_amount.label('xinyong_amount'),
            df_jiaoyi.c.dfjiaoyi_num.label('dfjiaoyi_num'),
            df_jiaoyi.c.dfjiaoyi_amount.label('dfjiaoyi_amount'),
            jiaoyi_qx.c.wraw_num.label('wraw_num'),
            jiaoyi_qx.c.wraw_amount.label('wraw_amount'),
            jiaoyi_qx.c.wrdraw_amount_sxf.label('wrdraw_amount_sxf'),
            jiaoyi_jy.c.jiaoyi_num.label('jiaoyi_num'),
            jiaoyi_jy.c.jiaoyi_amount.label('jiaoyi_amount'),
            jiaoyi_jy.c.jiaoyi_amount_service.label('jiaoyi_amount_service'),
            jiaoyi_jy.c.jiaoyi_amount_agents.label('jiaoyi_amount_agents'),
            df_agents_sxf.c.df_sxf.label('df_sxf'),
            (df_agents_sxf.c.df_sxf + jiaoyi_jy.c.jiaoyi_amount_service + jiaoyi_qx.c.wrdraw_amount_sxf - jiaoyi_jy.c.jiaoyi_amount_agents).label('sunyi')
        )

        res = res.all()

        return res
