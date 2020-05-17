from sqlalchemy import func,and_
from app.models.onlinetrades_dao import OnlinetradesDao
from app.models import db
from app.models.merchant_dao import MerchantDao
from app.models.withdraw_dao import WithdrawDao
import datetime,time
from app.api_0_1.utils import SECONDS_PER_DAY
from app.service.serviceutils.get_data_utils import getData
from sqlalchemy import literal

class GetResports():
    def __init__(self):
        res = getData()
        self.todaydata = res['today']
        self.yesterday_start = res['yesterday_start']
        self.yesterday_end = res['yesterday_end']
        self.thisweek_start = res['thisweek_start']
        self.thisweek_end = res['thisweek_end']
        self.thismonth_start = res['thismonth_start']
        self.thismonth_end = res['thismonth_end']

    def get_resports_info(self):
        todaydata = self.todaydata
        yesterday_start = self.yesterday_start
        yesterday_end = self.yesterday_end
        thisweek_start = self.thisweek_start
        thisweek_end = self.thisweek_end
        thismonth_start = self.thismonth_start
        thismonth_end = self.thismonth_end


        # 查询会员

        # 会员代付今日，交易记录今日
        mer_o_day = db.session.query(
            literal(0).label('merber'),
            func.coalesce(func.sum(OnlinetradesDao.bank_amount),0).label('bank_amount_day')
        ).filter(and_(
            OnlinetradesDao.audit_time >= self.todaydata,
            OnlinetradesDao.state == 2
        ))
        mer_o_day = mer_o_day.subquery()

        mer_d_day = db.session.query(
            literal(0).label('merber'),
            func.coalesce(func.sum(WithdrawDao.amount),0).label('withdraw_amount_day')
        ).filter(and_(
            WithdrawDao.audit_time >= self.todaydata,
            WithdrawDao.state == 2
        ))
        mer_d_day = mer_d_day.subquery()

        # 会员代付昨日，交易记录昨日
        mer_o_yes = db.session.query(
            literal(0).label('merber'),
            func.coalesce(func.sum(OnlinetradesDao.bank_amount),0).label('bank_amount_yes')
        ).filter(and_(
            OnlinetradesDao.audit_time >= self.yesterday_start,
            OnlinetradesDao.audit_time < self.yesterday_end,
            OnlinetradesDao.state == 2
        ))
        mer_o_yes = mer_o_yes.subquery()

        mer_d_yes = db.session.query(
            literal(0).label('merber'),
            func.coalesce(func.sum(WithdrawDao.amount),0).label('withdraw_amount_yes')
        ).filter(and_(
            WithdrawDao.audit_time >= self.yesterday_start,
            WithdrawDao.audit_time < self.yesterday_end,
            WithdrawDao.state == 2
        ))
        mer_d_yes = mer_d_yes.subquery()

        # 会员代付本周，交易记录本周
        mer_o_thisweek = db.session.query(
            literal(0).label('merber'),
            func.coalesce(func.sum(OnlinetradesDao.bank_amount),0).label('bank_amount_thisweek')
        ).filter(and_(
            OnlinetradesDao.audit_time >= self.thisweek_start,
            OnlinetradesDao.audit_time < self.thisweek_end,
            OnlinetradesDao.state == 2
        ))
        mer_o_thisweek = mer_o_thisweek.subquery()

        mer_d_thisweek = db.session.query(
            literal(0).label('merber'),
            func.coalesce(func.sum(WithdrawDao.amount),0).label('withdraw_amount_thisweek')
        ).filter(and_(
            WithdrawDao.audit_time >= self.thisweek_start,
            WithdrawDao.audit_time < self.thisweek_end,
            WithdrawDao.state == 2
        ))
        mer_d_thisweek = mer_d_thisweek.subquery()

        # 会员代付本月，交易记录本月
        mer_o_thismonth= db.session.query(
            literal(0).label('merber'),
            func.coalesce(func.sum(OnlinetradesDao.bank_amount),0).label('bank_amount_thismonth')
        ).filter(and_(
            OnlinetradesDao.audit_time >= self.thismonth_start,
            OnlinetradesDao.audit_time < self.thismonth_end,
            OnlinetradesDao.state == 2
        ))
        mer_o_thismonth = mer_o_thismonth.subquery()

        mer_d_thismonth = db.session.query(
            literal(0).label('merber'),
            func.coalesce(func.sum(WithdrawDao.amount),0).label('withdraw_amount_thismonth')
        ).filter(and_(
            WithdrawDao.audit_time >= self.thismonth_start,
            WithdrawDao.audit_time < self.thismonth_end,
            WithdrawDao.state == 2
        ))
        mer_d_thismonth = mer_d_thismonth.subquery()

        mer = db.session.query(
            literal('9518').label('name'),
            mer_o_day.c.merber,
            mer_o_day.c.bank_amount_day.label('bank_amount_day_member'),
            mer_d_day.c.withdraw_amount_day.label('withdraw_amount_day_member'),
            mer_o_yes.c.bank_amount_yes.label('bank_amount_yes_member'),
            mer_d_yes.c.withdraw_amount_yes.label('withdraw_amount_yes_member'),
            mer_o_thisweek.c.bank_amount_thisweek.label('bank_amount_thisweek_member'),
            mer_d_thisweek.c.withdraw_amount_thisweek.label('withdraw_amount_thisweek_member'),
            mer_o_thismonth.c.bank_amount_thismonth.label('bank_amount_thismonth_member'),
            mer_d_thismonth.c.withdraw_amount_thismonth.label('withdraw_amount_thismonth_member'),
        )
        print(mer.all())
        mer = mer.subquery()







        # 查询代理

        # 代理代付今日，交易记录今日
        agent_o_day = db.session.query(
            literal(1).label('agent'),
            func.coalesce(func.sum(OnlinetradesDao.real_cost_agent),0).label('cost_agent_day')
        ).filter(and_(
            OnlinetradesDao.audit_time >= self.todaydata,
            OnlinetradesDao.state == 2
        ))
        agent_o_day = agent_o_day.subquery()

        agent_o_day_service = db.session.query(
            literal(1).label('agent'),
            func.coalesce(func.sum(OnlinetradesDao.real_cost_service),0).label('cost_agent_service_day')
        ).filter(and_(
            OnlinetradesDao.audit_time >= self.todaydata,
            OnlinetradesDao.state == 2
        ))
        agent_o_day_service = agent_o_day_service.subquery()

        agent_d_day = db.session.query(
            literal(1).label('agent'),
            func.coalesce(func.sum(WithdrawDao.wrdraw_amount),0).label('withdraw_amount_day')
        ).filter(and_(
            WithdrawDao.audit_time >= self.todaydata,
            WithdrawDao.state == 2
        ))
        agent_d_day = agent_d_day.subquery()



        # 代理代付昨日，交易记录昨日
        agent_o_yes = db.session.query(
            literal(1).label('agent'),
            func.coalesce(func.sum(OnlinetradesDao.real_cost_agent),0).label('cost_agent_yes')
        ).filter(and_(
            OnlinetradesDao.audit_time >= self.yesterday_start,
            OnlinetradesDao.audit_time < self.yesterday_end,
            OnlinetradesDao.state == 2
        ))
        agent_o_yes = agent_o_yes.subquery()

        agent_o_yes_service = db.session.query(
            literal(1).label('agent'),
            func.coalesce(func.sum(OnlinetradesDao.real_cost_service),0).label('cost_agent_service_yes')
        ).filter(and_(
            OnlinetradesDao.audit_time >= self.yesterday_start,
            OnlinetradesDao.audit_time < self.yesterday_end,
            OnlinetradesDao.state == 2
        ))
        agent_o_yes_service = agent_o_yes_service.subquery()


        agent_d_yes = db.session.query(
            literal(1).label('agent'),
            func.coalesce(func.sum(WithdrawDao.wrdraw_amount),0).label('withdraw_amount_yes')
        ).filter(and_(
            WithdrawDao.audit_time >= self.yesterday_start,
            WithdrawDao.audit_time < self.yesterday_end,
            WithdrawDao.state == 2
        ))
        agent_d_yes = agent_d_yes.subquery()

        # 代理代付本周，交易记录本周
        agent_o_thisweek = db.session.query(
            literal(1).label('agent'),
            func.coalesce(func.sum(OnlinetradesDao.real_cost_agent),0).label('cost_agent_thisweek')
        ).filter(and_(
            OnlinetradesDao.audit_time >= self.thisweek_start,
            OnlinetradesDao.audit_time < self.thisweek_end,
            OnlinetradesDao.state == 2
        ))
        agent_o_thisweek = agent_o_thisweek.subquery()

        agent_o_thisweek_service = db.session.query(
            literal(1).label('agent'),
            func.coalesce(func.sum(OnlinetradesDao.real_cost_service),0).label('cost_agent_service_thisweek')
        ).filter(and_(
            OnlinetradesDao.audit_time >= self.thisweek_start,
            OnlinetradesDao.audit_time < self.thisweek_end,
            OnlinetradesDao.state == 2
        ))
        agent_o_thisweek_service = agent_o_thisweek_service.subquery()

        agent_d_thisweek = db.session.query(
            literal(1).label('agent'),
            func.coalesce(func.sum(WithdrawDao.wrdraw_amount),0).label('withdraw_amount_thisweek')
        ).filter(and_(
            WithdrawDao.audit_time >= self.thisweek_start,
            WithdrawDao.audit_time < self.thisweek_end,
            WithdrawDao.state == 2
        ))
        agent_d_thisweek = agent_d_thisweek.subquery()

        # 代理代付本月，交易记录本月
        agent_o_thismonth = db.session.query(
            literal(1).label('agent'),
            func.coalesce(func.sum(OnlinetradesDao.real_cost_agent),0).label('cost_agent_thismonth')
        ).filter(and_(
            OnlinetradesDao.audit_time >= self.thismonth_start,
            OnlinetradesDao.audit_time < self.thismonth_end,
            OnlinetradesDao.state == 2
        ))
        agent_o_thismonth = agent_o_thismonth.subquery()

        agent_o_thismonth_service = db.session.query(
            literal(1).label('agent'),
            func.coalesce(func.sum(OnlinetradesDao.real_cost_service),0).label('cost_agent_service_thismonth')
        ).filter(and_(
            OnlinetradesDao.audit_time >= self.thismonth_start,
            OnlinetradesDao.audit_time < self.thismonth_end,
            OnlinetradesDao.state == 2
        ))
        agent_o_thismonth_service = agent_o_thismonth_service.subquery()

        agent_d_thismonth = db.session.query(
            literal(1).label('agent'),
            func.coalesce(func.sum(WithdrawDao.wrdraw_amount),0).label('withdraw_amount_thismonth')
        ).filter(and_(
            WithdrawDao.audit_time >= self.thismonth_start,
            WithdrawDao.audit_time < self.thismonth_end,
            WithdrawDao.state == 2
        ))
        agent_d_thismonth = agent_d_thismonth.subquery()

        agent = db.session.query(
            literal('9518').label('name'),
            mer_o_day.c.merber,
            agent_o_day.c.cost_agent_day.label('cost_agent_day'),
            agent_o_day_service.c.cost_agent_service_day.label('cost_agent_service_day'),
            agent_d_day.c.withdraw_amount_day.label('withdraw_agent_amount_day'),
            agent_o_yes.c.cost_agent_yes.label('cost_agent_yes'),
            agent_o_yes_service.c.cost_agent_service_yes.label('cost_agent_service_yes'),
            agent_d_yes.c.withdraw_amount_yes.label('withdraw_agent_amount_yes'),
            agent_o_thisweek.c.cost_agent_thisweek.label('cost_agent_thisweek'),
            agent_o_thisweek_service.c.cost_agent_service_thisweek.label('cost_agent_service_thisweek'),
            agent_d_thisweek.c.withdraw_amount_thisweek.label('withdraw_agent_amount_thisweek'),
            agent_o_thismonth.c.cost_agent_thismonth.label('cost_agent_thismonth'),
            agent_o_thismonth_service.c.cost_agent_service_thismonth.label('cost_agent_service_thismonth'),
            agent_d_thismonth.c.withdraw_amount_thismonth.label('withdraw_agent_amount_thismonth'),
        )
        agent = agent.subquery()


        mer_and_agent = db.session.query(
            agent.c.cost_agent_day.label('cost_agent_day'),
            agent.c.cost_agent_service_day.label('cost_agent_service_day'),
            agent.c.withdraw_agent_amount_day.label('withdraw_agent_amount_day'),
            agent.c.cost_agent_yes.label('cost_agent_yes'),
            agent.c.cost_agent_service_yes.label('cost_agent_service_yes'),
            agent.c.withdraw_agent_amount_yes.label('withdraw_agent_amount_yes'),
            agent.c.cost_agent_thisweek.label('cost_agent_thisweek'),
            agent.c.cost_agent_service_thisweek.label('cost_agent_service_thisweek'),
            agent.c.withdraw_agent_amount_thisweek.label('withdraw_agent_amount_thisweek'),
            agent.c.cost_agent_thismonth.label('cost_agent_thismonth'),
            agent.c.cost_agent_service_thismonth.label('cost_agent_service_thismonth'),
            agent.c.withdraw_agent_amount_thismonth.label('withdraw_agent_amount_thismonth'),
            mer.c.bank_amount_day_member.label('bank_amount_day_member'),
            mer.c.withdraw_amount_day_member.label('withdraw_amount_day_member'),
            mer.c.bank_amount_yes_member.label('bank_amount_yes_member'),
            mer.c.withdraw_amount_yes_member.label('withdraw_amount_yes_member'),
            mer.c.bank_amount_thisweek_member.label('bank_amount_thisweek_member'),
            mer.c.withdraw_amount_thisweek_member.label('withdraw_amount_thisweek_member'),
            mer.c.bank_amount_thismonth_member.label('bank_amount_thismonth_member'),
            mer.c.withdraw_amount_thismonth_member.label('withdraw_amount_thismonth_member'),
            (agent.c.withdraw_agent_amount_day + agent.c.cost_agent_service_day - agent.c.cost_agent_day).label('pt_day'),
            (agent.c.withdraw_agent_amount_yes + agent.c.cost_agent_service_yes - agent.c.cost_agent_yes).label('pt_yes'),
            (agent.c.withdraw_agent_amount_thisweek + agent.c.cost_agent_service_thisweek - agent.c.cost_agent_thisweek).label('pt_thisweek'),
            (agent.c.withdraw_agent_amount_thismonth + agent.c.cost_agent_service_thismonth - agent.c.cost_agent_thismonth).label('pt_thismonth'),
        )

        mer_and_agent = mer_and_agent.all()
        return mer_and_agent