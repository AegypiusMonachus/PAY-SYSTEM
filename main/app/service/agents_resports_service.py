from sqlalchemy import func,and_
from app.models.onlinetrades_dao import OnlinetradesDao
from app.models import db
from app.models.merchant_dao import MerchantDao
from app.models.withdraw_dao import WithdrawDao
import datetime,time
from app.api_0_1.utils import SECONDS_PER_DAY

class AgentsResportsService():

    def __init__(self):
        pass


    def get_data_agents_resports(self,args=None,page=None,per_page=None,critern_name=None,critern_wraw=None):
        res_total_completed = db.session.query(
            OnlinetradesDao.user_name,
            func.sum(OnlinetradesDao.real_cost_agent).label('cost_agent_completed')
        ).group_by(OnlinetradesDao.user_name).filter(*args).filter(OnlinetradesDao.state == 2).subquery()
        res_total_hang = db.session.query(
            OnlinetradesDao.user_name,
            func.sum(OnlinetradesDao.real_cost_agent).label('cost_agent_hang')
        ).group_by(OnlinetradesDao.user_name).filter(*args).filter(OnlinetradesDao.state == 1).subquery()

        res_total_completed_wraw = db.session.query(
            WithdrawDao.mer_name,
            func.sum(WithdrawDao.wrdraw_amount).label('wrdraw_amount_completed')
        ).group_by(WithdrawDao.mer_name).filter(*critern_wraw).filter(WithdrawDao.state == 2).subquery()
        res_total_hang_wraw = db.session.query(
            WithdrawDao.mer_name,
            func.sum(WithdrawDao.wrdraw_amount).label('wrdraw_amount_hang')
        ).group_by(WithdrawDao.mer_name).filter(*critern_wraw).filter(WithdrawDao.state == 1).subquery()

        res_total = db.session.query(
            OnlinetradesDao.user_name,
            func.sum(OnlinetradesDao.real_cost_agent).label('cost_agent')
        ).group_by(OnlinetradesDao.user_name).filter(*args).subquery()

        res_total_wraw = db.session.query(
            WithdrawDao.mer_name,
            func.sum(WithdrawDao.wrdraw_amount).label('wrdraw_amount')
        ).group_by(WithdrawDao.mer_name).filter(*critern_wraw).filter(WithdrawDao.state.in_([1,2])).subquery()

        q = db.session.query(
            res_total.c.user_name.label('user_name'),
            res_total.c.cost_agent.label('cost_agent'),
            res_total_completed.c.cost_agent_completed.label('cost_agent_completed'),
            res_total_hang.c.cost_agent_hang.label('cost_agent_hang')
        )

        q = q.outerjoin(res_total_completed, res_total_completed.c.user_name == res_total.c.user_name)
        q = q.outerjoin(res_total_hang, res_total_hang.c.user_name == res_total.c.user_name)

        q = q.subquery()

        q2 = db.session.query(
            res_total_wraw.c.mer_name.label('user_name'),
            res_total_completed_wraw.c.wrdraw_amount_completed.label('wrdraw_amount_completed'),
            res_total_hang_wraw.c.wrdraw_amount_hang.label('wrdraw_amount_hang'),
            res_total_wraw.c.wrdraw_amount.label('wrdraw_amount'),
        )
        q2 = q2.outerjoin(res_total_completed_wraw, res_total_completed_wraw.c.mer_name == res_total_wraw.c.mer_name)
        q2 = q2.outerjoin(res_total_hang_wraw, res_total_hang_wraw.c.mer_name == res_total_wraw.c.mer_name)
        q2 = q2.subquery()

        res = db.session.query(
            MerchantDao.parent_name,
            func.sum(q.c.cost_agent).label('cost_agent'),
            func.sum(q.c.cost_agent_completed).label('cost_agent_completed'),
            func.sum(q.c.cost_agent_hang).label('cost_agent_hang'),
            func.sum(q2.c.wrdraw_amount_completed).label('wrdraw_amount_completed'),
            func.sum(q2.c.wrdraw_amount_hang).label('wrdraw_amount_hang'),
            func.sum(q2.c.wrdraw_amount).label('wrdraw_amount'),
        ).group_by(MerchantDao.parent_name).filter(*critern_name)
        res = res.outerjoin(q,q.c.user_name == MerchantDao.username)
        res = res.outerjoin(q2, q2.c.user_name == MerchantDao.username)
        res = res.paginate(page, per_page, error_out=False)
        return res




    def get_data_agents_resports_merchat(self,args=None,page=None,per_page=None):
        res_total_completed = db.session.query(
            OnlinetradesDao.user_name,
            func.sum(OnlinetradesDao.real_cost_agent).label('cost_agent_completed')
        ).group_by(OnlinetradesDao.user_name).filter(*args).filter(OnlinetradesDao.state == 2).subquery()
        res_total_hang = db.session.query(
            OnlinetradesDao.user_name,
            func.sum(OnlinetradesDao.real_cost_agent).label('cost_agent_hang')
        ).group_by(OnlinetradesDao.user_name).filter(*args).filter(OnlinetradesDao.state == 1).subquery()

        res_total = db.session.query(
            OnlinetradesDao.user_name,
            func.sum(OnlinetradesDao.real_cost_agent).label('cost_agent')
        ).group_by(OnlinetradesDao.user_name).filter(*args).subquery()
        q = db.session.query(
            res_total.c.user_name,
            res_total.c.cost_agent,
            res_total_completed.c.cost_agent_completed,
            res_total_hang.c.cost_agent_hang,
        )

        q = q.outerjoin(res_total_completed, res_total_completed.c.user_name == res_total.c.user_name)
        q = q.outerjoin(res_total_hang, res_total_hang.c.user_name == res_total.c.user_name)
        res = q.paginate(page, per_page, error_out=False)
        return res



    def get_data_agents_resports_total(self,args=None,critern_name=None,critern_wraw=None):
        res_total_completed = db.session.query(
            OnlinetradesDao.user_name,
            func.sum(OnlinetradesDao.real_cost_agent).label('cost_agent_completed')
        ).group_by(OnlinetradesDao.user_name).filter(*args).filter(OnlinetradesDao.state == 2).subquery()
        res_total_hang = db.session.query(
            OnlinetradesDao.user_name,
            func.sum(OnlinetradesDao.real_cost_agent).label('cost_agent_hang')
        ).group_by(OnlinetradesDao.user_name).filter(*args).filter(OnlinetradesDao.state == 1).subquery()

        res_total_completed_wraw = db.session.query(
            WithdrawDao.mer_name,
            func.sum(WithdrawDao.wrdraw_amount).label('wrdraw_amount_completed')
        ).group_by(WithdrawDao.mer_name).filter(*critern_wraw).filter(WithdrawDao.state == 2).subquery()
        res_total_hang_wraw = db.session.query(
            WithdrawDao.mer_name,
            func.sum(WithdrawDao.wrdraw_amount).label('wrdraw_amount_hang')
        ).group_by(WithdrawDao.mer_name).filter(*critern_wraw).filter(WithdrawDao.state == 1).subquery()

        res_total = db.session.query(
            OnlinetradesDao.user_name,
            func.sum(OnlinetradesDao.real_cost_agent).label('cost_agent')
        ).group_by(OnlinetradesDao.user_name).filter(*args).subquery()

        res_total_wraw = db.session.query(
            WithdrawDao.mer_name,
            func.sum(WithdrawDao.wrdraw_amount).label('wrdraw_amount')
        ).group_by(WithdrawDao.mer_name).filter(*critern_wraw).filter(WithdrawDao.state.in_([1,2])).subquery()

        q = db.session.query(
            res_total.c.user_name.label('user_name'),
            res_total.c.cost_agent.label('cost_agent'),
            res_total_completed.c.cost_agent_completed.label('cost_agent_completed'),
            res_total_hang.c.cost_agent_hang.label('cost_agent_hang'),
        )

        q = q.outerjoin(res_total_completed, res_total_completed.c.user_name == res_total.c.user_name)
        q = q.outerjoin(res_total_hang, res_total_hang.c.user_name == res_total.c.user_name)
        q = q.subquery()

        q2 = db.session.query(
            res_total_wraw.c.mer_name.label('user_name'),
            res_total_completed_wraw.c.wrdraw_amount_completed.label('wrdraw_amount_completed'),
            res_total_hang_wraw.c.wrdraw_amount_hang.label('wrdraw_amount_hang'),
            res_total_wraw.c.wrdraw_amount.label('wrdraw_amount'),
        )
        q2 = q2.outerjoin(res_total_completed_wraw, res_total_completed_wraw.c.mer_name == res_total_wraw.c.mer_name)
        q2 = q2.outerjoin(res_total_hang_wraw, res_total_hang_wraw.c.mer_name == res_total_wraw.c.mer_name)
        q2 = q2.subquery()

        res = db.session.query(
            MerchantDao.parent_name,
            func.sum(q.c.cost_agent).label('cost_agent'),
            func.sum(q.c.cost_agent_completed).label('cost_agent_completed'),
            func.sum(q.c.cost_agent_hang).label('cost_agent_hang'),
            func.sum(q2.c.wrdraw_amount_completed).label('wrdraw_amount_completed'),
            func.sum(q2.c.wrdraw_amount_hang).label('wrdraw_amount_hang'),
            func.sum(q2.c.wrdraw_amount).label('wrdraw_amount'),
        ).group_by(MerchantDao.parent_name).filter(*critern_name)
        res = res.outerjoin(q,q.c.user_name == MerchantDao.username)
        res = res.outerjoin(q2, q2.c.user_name == MerchantDao.username)
        res = res.subquery()
        res_total = db.session.query(
            func.sum(res.c.cost_agent).label('cost_agent_total'),
            func.sum(res.c.cost_agent_completed).label('cost_agent_completed_total'),
            func.sum(res.c.cost_agent_hang).label('cost_agent_hang_total'),
            func.sum(res.c.wrdraw_amount_completed).label('wrdraw_amount_completed'),
            func.sum(res.c.wrdraw_amount_hang).label('wrdraw_amount_hang'),
            func.sum(res.c.wrdraw_amount).label('wrdraw_amount'),

        )
        res_total = res_total.all()
        return res_total
    
    
    def get_data_agents_resports_total_merchart(self,args=None,critern_name=None,critern_parent=None):


        # 查询总的
        res_total = db.session.query(
            OnlinetradesDao.user_name.label('user_name'),
            func.sum(OnlinetradesDao.real_cost_agent).label('cost_agent'),
            func.count(OnlinetradesDao.id).label('agents_number')
        ).group_by(OnlinetradesDao.user_name).filter(*args)
        res_total = res_total.subquery()

        res_total_amount = db.session.query(
            OnlinetradesDao.user_name.label('user_name'),
            func.sum(OnlinetradesDao.amount).label('cost_agent_amount')
        ).group_by(OnlinetradesDao.user_name).filter(*args).filter(OnlinetradesDao.state == 2)
        res_total_amount = res_total_amount.subquery()

        # 查询今日
        today = datetime.date.today()
        zeroPointToday = int(time.mktime(today.timetuple()))
        endPointToday = zeroPointToday + SECONDS_PER_DAY
        res_day = db.session.query(
            OnlinetradesDao.user_name.label('user_name'),
            func.sum(OnlinetradesDao.amount).label('sum_amount_day')
        ).filter(and_(
            OnlinetradesDao.audit_time >= zeroPointToday,
            OnlinetradesDao.audit_time <= endPointToday
        )).group_by(OnlinetradesDao.user_name)
        res_day = res_day.outerjoin(MerchantDao, MerchantDao.code == OnlinetradesDao.mer_code)
        res_day = res_day.subquery()



        # 查讯昨日
        endPointToday = zeroPointToday + SECONDS_PER_DAY
        endPointYestoday = zeroPointToday
        # print('昨日%s' % endPointYestoday)
        zeroPointYestoday = endPointYestoday - 60 * 60 * 24
        res_yes = db.session.query(
            OnlinetradesDao.user_name.label('user_name'),
            func.sum(OnlinetradesDao.amount).label('sum_amount_yes')
        ).filter(and_(
            OnlinetradesDao.audit_time >= zeroPointYestoday,
            OnlinetradesDao.audit_time <= endPointYestoday
        )).group_by(OnlinetradesDao.user_name)
        res_yes = res_yes.outerjoin(MerchantDao, MerchantDao.code == OnlinetradesDao.mer_code)
        res_yes = res_yes.subquery()



        q = db.session.query(
            res_total.c.user_name.label('user_name'),
            res_total.c.cost_agent.label('cost_agent'),
            res_total_amount.c.cost_agent_amount.label('cost_agent_amount'),
            res_total.c.agents_number.label('agents_number'),
            res_day.c.sum_amount_day.label('sum_amount_day'),
            res_yes.c.sum_amount_yes.label('sum_amount_yes')
        )
        q = q.outerjoin(res_day, res_day.c.user_name == res_total.c.user_name)
        q = q.outerjoin(res_yes, res_yes.c.user_name == res_total.c.user_name)
        q = q.outerjoin(res_total_amount, res_total_amount.c.user_name == res_total.c.user_name)

        q = q.subquery()


        res = db.session.query(
            MerchantDao.parent_name.label('username'),
            func.sum(q.c.cost_agent).label('cost_agent'),
            func.sum(q.c.cost_agent_amount).label('cost_agent_amount'),
            func.sum(q.c.agents_number).label('agents_number'),
            func.sum(q.c.sum_amount_day).label('sum_amount_day'),
            func.sum(q.c.sum_amount_yes).label('sum_amount_yes'),
        ).group_by(MerchantDao.parent_name).filter(*critern_name)
        res = res.outerjoin(q,q.c.user_name == MerchantDao.username)
        res = res.subquery()


        res_res = db.session.query(
            MerchantDao.username.label('username'),
            MerchantDao.amount.label('amount'),
            res.c.cost_agent.label('cost_agent'),
            res.c.cost_agent_amount.label('cost_agent_amount'),
            res.c.agents_number.label('agents_number'),
            res.c.sum_amount_day.label('sum_amount_day'),
            res.c.sum_amount_yes.label('sum_amount_yes'),
        ).filter(*critern_parent)
        res_res = res_res.outerjoin(res, res.c.username == MerchantDao.username)
        res_res = res_res.all()
        return res_res
