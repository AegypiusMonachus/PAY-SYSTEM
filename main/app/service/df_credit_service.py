from app.models.df_bank_dao import DfBanks
from app.models import db
from app.common import creat_order_no
from app.models.df_trade_dao import DfTradeRechargeDao,DfTradeAgentsDao,DfTradeDao
from app.models.merchant_dao import MerchantDao
from decimal import Decimal
import decimal
from app.common import keep_two_del
from flask import current_app
from flask_restful import abort
from flask.json import jsonify
from .serviceutils.utils import encrypt_md5,merRange,rando
import time



class DfCreditService():

	def __init__(self):
		pass

	# 验证
	def ver_merchart(self,pas,salt):
		# print(encrypt_md5(pas))
		# print('*************************************************')
		password = encrypt_md5(pas + str(salt))

		return password
	# 充值信用额度
	def save_amount(self,m_args):
		m_args['state'] = 1
		mer_codes = db.session.query(MerchantDao.id,MerchantDao.code,MerchantDao.amount,MerchantDao.type,MerchantDao.username).filter(MerchantDao.code == m_args['mer_code']).first()
		if mer_codes is None:
			return {
				'success': False,
				'error_code': 8001,
				'error_msg': '该订单错误，请重新申请'
			}
		if mer_codes.type != 3:
			return {
				'success': False,
				'error_code': 8002,
				'error_msg': '该用户类型不支持'
			}
		order_no = creat_order_no(102, mer_codes.id)
		mer_code = m_args['mer_code']

		m_args['order_no'] = order_no
		m_args['action_time'] = int(time.time())
		m_args['mer_code'] = mer_code
		m_args['username'] = mer_codes.username
		try:
			dao = DfTradeRechargeDao(**m_args)
			db.session.add(dao)
			db.session.commit()
			return {
				'success': True
			}
		except:
			db.session.rollback()
			db.session.remove()
			return {
				'success': False,
				'error_code': 401,
				'error_msg': '该订单申请错误，请重新申请'
			}


	# 充值信用额度确认
	def confirm_amount(self,m_args):
		res = db.session.query(
			DfTradeRechargeDao.amount.label('dfamount'),
			DfTradeRechargeDao.state,
			DfTradeRechargeDao.mer_code,
			MerchantDao.amount
		).filter(
			DfTradeRechargeDao.order_no == m_args['order_no']
		)
		res = res.outerjoin(MerchantDao,MerchantDao.code == DfTradeRechargeDao.mer_code)
		res = res.first()
		if res is not None:
			if res.state == 1:
				if m_args['state'] == 2:
					me_args = {}
					df_args = {}
					if res.dfamount is None:
						dfamount = 0
					else:
						dfamount = res.dfamount
					if res.amount is None:
						amount = 0
					else:
						amount = res.amount
					me_args['amount'] = dfamount + amount
					df_args['state'] = m_args['state']
					df_args['audit_time'] = int(time.time())
					df_args['audit_name'] = m_args['audit_name']
					try:
						MerchantDao.query.filter(MerchantDao.code == res.mer_code).update(me_args)
						DfTradeRechargeDao.query.filter(DfTradeRechargeDao.order_no == m_args['order_no']).update(df_args)
						db.session.commit()
						return {
							'success': True
						}
					except:
						db.session.rollback()
						db.session.remove()
						return {
							'success': False,
							'error_code': 401,
							'error_msg': '该订单出错'
						}
				else:
					df_args = {}
					df_args['state'] = m_args['state']
					df_args['audit_time'] = int(time.time())
					df_args['audit_name'] = m_args['audit_name']
					try:
						DfTradeRechargeDao.query.filter(DfTradeRechargeDao.order_no == m_args['order_no']).update(df_args)
						db.session.commit()
						return {
							'success': True
						}
					except:
						db.session.rollback()
						db.session.remove()
						return {
							'success': False,
							'error_code': 401,
							'error_msg': '该订单出错'
						}
			else:
				return {
					'success': False,
					'errorCode': 418,
					'errorMsg': '该订单状态错误'
				}