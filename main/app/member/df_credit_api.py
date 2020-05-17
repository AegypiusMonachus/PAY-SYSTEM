from flask_restful import Resource
from app.service.df_credit_service import DfCreditService
from app.agentspay.parsers.save_wrawamount import savewithdrawalparser,savewithdrawalputparser,getwithdrawalparser
from flask import g
from app.models.df_trade_dao import DfTradeRechargeDao
from app.service.df_get_credit_service import DfGetCreditSer
from app.common import keep_two_del
from app.api_0_1.common import make_response
from app.models import db
from app.models.merchant_dao import MerchantDao
from app.models.df_agent_rate_dao import DfAgentRate
from app.models.df_trade_dao import DfTradeDao

class DfCredit(Resource):
	def get(self):
		m_args = getwithdrawalparser.parse_args(strict=True)
		critern = set()
		if g.current_member:
			if int(g.current_member.type) == 3:
				username = g.current_member.username
				critern.add(DfTradeRechargeDao.username == username)
			if int(g.current_member.type) == 4:
				username = g.current_member.username
				res = db.session.query(DfAgentRate.mer_username).filter(DfAgentRate.agent_name == username).all()
				result = []
				for i in res:
					result.append(i[0])
				critern.add(DfTradeRechargeDao.username.in_(result))
		if m_args['action_begin_time'] is not None:
			critern.add(DfTradeRechargeDao.action_time >= m_args['action_begin_time'])

		if m_args['action_end_time'] is not None:
			critern.add(DfTradeRechargeDao.action_time <= m_args['action_end_time'])

		if m_args['audit_begin_time'] is not None:
			critern.add(DfTradeRechargeDao.audit_time >= m_args['audit_begin_time'])

		if m_args['audit_end_time'] is not None:
			critern.add(DfTradeRechargeDao.audit_time <= m_args['audit_end_time'])

		if m_args['state'] is not None:
			critern.add(DfTradeRechargeDao.state == m_args['state'])

		args = DfGetCreditSer.get_data(self, critern, m_args['page'], m_args['page_size'])
		result = []
		for i in args.items:
			if i.amount is not None:
				amount = float('%.2f' % keep_two_del(i.amount))
			else:
				amount = 0

			# if i.real_amount is not None:
			# 	real_amount = float('%.2f' % keep_two_del(i.real_amount))
			# else:
			# 	real_amount = 0
			result.append({
				'id': i.id,
				'order_no': i.order_no,
				'amount': amount,
				'real_amount': amount,
				'action_time': i.action_time,
				'audit_time': i.audit_time,
				'audit_name': i.audit_name,
				'state': i.state,
				'username': i.username,
				'remark': i.remark,
			})
		return make_response(result, page=args.page, pages=args.pages, total=args.total)



	def post(self):
		m_args = savewithdrawalparser.parse_args(strict=True)
		password = m_args.pop('password')
		if g.current_member.username:
			m_args['action_name'] = g.current_member.username
		else:
			return {"success": False, "error_code": 999}

		pas = db.session.query(MerchantDao.password,MerchantDao.salt).filter(MerchantDao.username == m_args['action_name']).first()

		res = DfCreditService()
		args = res.save_amount(m_args)
		return args
		# passwo = res.ver_merchart(password,pas.salt)
		# if passwo == pas.password:
		# 	args = res.save_amount(m_args)
		#
		# 	return args
		# else:
		# 	return {"success": False, "error_code": 998}


	def put(self):
		m_args = savewithdrawalputparser.parse_args(strict=True)
		if g.current_member.username:
			m_args['audit_name'] = g.current_member.username
		else:
			return {"success": False, "error_code": 999}
		res = DfCreditService()
		args = res.confirm_amount(m_args)
		return args