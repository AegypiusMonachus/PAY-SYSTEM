import json, hashlib, requests, time, random
from app.log import agentpaylogger
from app.common import creat_order_no
from app.models.df_bank_dao import DfBanks
from app.models import db
from app.models.df_trade_dao import DfTradeRechargeDao, DfTradeAgentsDao, DfTradeDao,DfTradeExpanDao
from app.models.merchant_dao import MerchantDao
from decimal import Decimal
import decimal
from app.common import keep_two_del,formatDecimal_two
from flask import current_app
from flask_restful import abort
from flask.json import jsonify
from .serviceutils.utils import encrypt_md5, merRange, rando
from app.models.df_submit_data_dao import DfSubData
from app.models.withdraw_dao import BankDao
from app.models.df_agent_rate_dao import DfAgentRate
from app.log import agentpayQuerylogger
from sqlalchemy import func,and_
from builtins import staticmethod


class WOlinetrideService():

	def __init__(self, args=None):
		self.context_subdata = DfSubData().get_data()
		self.context_merchart = MerchantDao().get_data(args['mer_code'])
		self.__bankcard = BankDao().get_bank(args['bankcard'])

	# 验证
	def ver_merchart(self, pas, salt):
		password = encrypt_md5(pas + str(salt))
		return password


	# 接收商户传递的数据
	def receive_withdrawal(self, m_args):
		try:
			m_args['amount'] = decimal.Decimal(m_args['amount'])
			if self.context_merchart is not None:
				mem = self.context_merchart
				if mem.type != 3:
					return {
						'success': False,
						'errorCode': 8002,
						'errorMsg': '商户编号错误'
					}
			else:
				return {
					'success': False,
					'error_code': 8002,
					'error_msg': '商户编号错误'
				}

			select_key = self.context_merchart.secret_key
			order_no = creat_order_no(8001, self.context_subdata.id)
			sxf = self.calculation_amount_sum(m_args['mer_code'], m_args['amount'])
			if mem.amount < m_args['amount'] + sxf:
				return {
					'success': False,
					'error_code': 8003,
					'error_msg': '余额不足'
				}
			state = 1
			m_str = ''
			args = {}
			bank_args = {}
			bank_args['order_no'] = order_no

			bank_args['org_order_no'] = m_args['org_order_no']
			bank_args['state'] = state
			sign = m_args.pop('sign')
			for k in sorted(m_args):
				args[k] = m_args[k]
				if m_args[k] is not None:
					m_str += '%s=%s&' % (k, m_args[k])
			m_str = m_str[:-1]
			m_str += select_key
			m_sign = self.get_sign(m_str)
			agentpaylogger.info('上游加密字符串:%s' % m_str)
			agentpaylogger.info('上游请求sign:%s' % sign)
			agentpaylogger.info('上游加密sign:%s' % m_sign)
			if m_sign == sign:
				m_args['order_no'] = order_no
				m_args['mem_amount'] = mem.amount
				m_args['mer_username'] = mem.username
				m_args['dongjie_amount'] = mem.dongjie_amount
				m_args['sxf'] = sxf
				in_service = self.insert_cash_reservice(m_args)
				data_args = {}
				data_args['mchntCd'] = self.context_subdata.code
				data_args['mchntPayforSsn'] = order_no
				data_args['cardName'] = m_args['name']
				data_args['cardNo'] = m_args['account_number']
				data_args['destAmount'] = float('%.2f' % keep_two_del(decimal.Decimal(m_args['amount']))) * 100
				data_args['bankCd'] = self.__bankcard
				if in_service is not None:
					return in_service
				data = {}
				data['order_no'] = order_no
				data['org_order_no'] = m_args['org_order_no']
				data['state'] = 1
				m_str = ''
				for k in sorted(data):
					if data[k] is not None:
						m_str += '%s=%s&' % (k, data[k])
				m_str = m_str[:-1]
				m_str += select_key
				m_sign_bank = self.get_sign(m_str)
				data['sign'] = m_sign_bank
				try:
					db.session.commit()
				except Exception as e:
					db.session.rollback()
					db.session.remove()
					agentpaylogger.error(e)
					agentpaylogger.exception(e)
					return {
						'success': False,
						'error_code': 8001,
						'error_msg': '代付失败'
					}
				return {
 					'success': True,
 					'data': data
 				}
# 				res = self.cash_withdrawal(data_args)
# 				if res is not None:
# 					if res['success'] == True:
# 						m_str_bank = ''
# 						for k in sorted(bank_args):
# 							if bank_args[k] is not None:
# 								m_str_bank += '%s=%s&' % (k, bank_args[k])
# 						m_str_bank = m_str_bank[:-1]
# 						m_str_bank += select_key
# 						m_sign_bank = self.get_sign(m_str_bank)
# 						bank_args['sign'] = m_sign_bank
# 						data = bank_args
# 						return {
# 							'success': True,
# 							'data': data
# 						}
# 					else:
# 						return {
# 							'success': False,
# 							'error_code': 8001,
# 							'error_msg': '代付失败'
# 						}
			else:
				return {
					'success': False,
					'error_code': 8004,
					'error_msg': '签名错误'
				}
		except Exception as e:
			agentpaylogger.exception(e)
			agentpaylogger.error(format(e))
			return {
				'success': False,
				'error_code': 8001,
				'error_msg': '代付失败'
			}

	# 代付申请
	def cash_withdrawal(self, data_args):
		select_key = self.context_subdata.select_key
		m_str = ''
		args = {}
		for k in sorted(data_args):
			args[k] = data_args[k]
			if data_args[k] is not None:
				m_str += '%s=%s&' % (k, data_args[k])
		m_str = m_str[:-1]
		m_str += select_key
		m_sign = self.get_sign(m_str)
		agentpaylogger.info('下游加密json:%s' % data_args)
		agentpaylogger.info('下游加密字符串:%s' % m_str)
		agentpaylogger.info('下游加密sign:%s' % m_sign)
		agentpaylogger.info('下游补发回调路由%s' % self.context_subdata.df_url)
		data_args['sign'] = m_sign
		res = json.loads(self.cash_post(data_args, self.context_subdata.df_url))
		agentpaylogger.info('下游补发回调路由返回信息%s' % res)
		data_args['state_code'] = res['code']
		if res['code'] == 200:
			in_cash = self.insert_cash_response(data_args)
			if in_cash is not None:
				return {
					'success': False,
					'error_code': 8001,
					'error_msg': '代付失败'
				}
			return {
				'success': True
			}

		else:
			in_cash = self.update_remove(data_args)
			return {
				'success': False,
				'error_code': 8001,
				'error_msg': '代付失败'
			}

	# 代付余额提现结果查询
	def get_send_withdrawal(self, m_args=None):
		pass

	def get_sign(self, m_str):
		md = hashlib.md5()
		md.update((m_str).encode())
		m_sign = md.hexdigest()

		return m_sign

	def cash_post(self, data_args, pay_url):
		headers = {'content-type': 'application/json'}
		r = requests.post(pay_url, data=json.dumps(data_args), headers=headers,timeout=5000)
		res = r.text
		agentpaylogger.info('请求地址  :  %s' %(pay_url))
		agentpaylogger.info('请求参数  :  %s' %(json.dumps(data_args)))
		agentpaylogger.info('请求返回  :  %s' %(res))
		return res

	def cash_get(self, str_r, pay_url):
		url = pay_url + '?%s' % str_r
		r = requests.get(url)
		res = r.text
		return res

	def insert_cash_reservice(self, m_args):
		args = {}
		args['mer_code'] = m_args['mer_code']
		args['mer_username'] = m_args['mer_username']
		args['org_order_no'] = m_args['org_order_no']
		args['order_no'] = m_args['order_no']
		args['account_name'] = m_args['name']
		args['account_no'] = m_args['account_number']
		args['amount'] = m_args['amount']
		args['action_time'] = int(time.time())
		args['sxf'] = m_args['sxf']
		args['type'] = 1
		args['bank_id'] = m_args['bankcard']
		args['state'] = 1
		a_args = {}
		if m_args['mem_amount'] is None:
			m_args['mem_amount'] = 0
		if m_args['amount'] is None:
			m_args['amount'] = 0
		if m_args['dongjie_amount'] is None:
			m_args['dongjie_amount'] = 0
		a_args['amount'] = m_args['mem_amount'] - m_args['amount'] - args['sxf']
		a_args['dongjie_amount'] = m_args['dongjie_amount'] + m_args['amount'] + args['sxf']
		e_args = {}
		m_args['amount'] = str(m_args['amount'])
		m_args.pop('mem_amount')
		m_args.pop('dongjie_amount')
		m_args.pop('sxf')
		e_args['org_order_no'] = m_args['org_order_no']
		e_args['order_no'] = m_args['order_no']
		e_args['mer_code'] = m_args['mer_code']
		e_args['expansion_data'] = m_args
		try:
			dao = DfTradeDao(**args)
			epan = DfTradeExpanDao(**e_args)
			MerchantDao.query.filter(MerchantDao.code == m_args['mer_code']).update(a_args)
			db.session.add(dao)
			db.session.add(epan)
			# db.session.commit()
		except Exception as e:
			db.session.rollback()
			db.session.remove()
			current_app.logger.exception(e)
			return {
				'success': False,
				'error_code': 8001,
				'error_msg': '代付失败'
			}

	# raise Exception(e)

	def insert_cash_response(self, data_args):
		args = {}
		args['mer_code'] = data_args['mchntCd']
		args['bankCd'] = data_args['bankCd']
		args['order_no'] = data_args['mchntPayforSsn']
		args['account_name'] = data_args['cardName']
		args['account_no'] = data_args['cardNo']
		if data_args['destAmount'] is None:
			data_args['destAmount'] = 0
		args['amount'] = data_args['destAmount'] / 100
		args['action_time'] = int(time.time())
		args['sign'] = data_args['sign']
		args['state'] = 1
		args['state_code'] = data_args['state_code']
		try:
			dao = DfTradeAgentsDao(**args)
			db.session.add(dao)
			db.session.commit()
		except Exception as e:
			db.session.rollback()
			db.session.remove()
			current_app.logger.exception(e)
			return {
				'success': False,
				'error_code': 8001,
				'error_msg': '代付失败'
			}

	# raise Exception(e)

	def update_cash_response(self, m_args):
		args = {}
		ams = {}
		args['state'] = 2
		args['audit_time'] = int(time.time())
		am = db.session.query(
			MerchantDao.amount,
			MerchantDao.dongjie_amount
		).filter(MerchantDao.code == m_args['mer_code']).first()
		dfam = db.session.query(
			DfTradeDao.order_no,
			DfTradeDao.org_order_no,
			DfTradeDao.mer_code,
			DfTradeDao.amount,
			DfTradeDao.action_time,
			DfTradeDao.audit_time,
			DfTradeDao.sxf,
			DfTradeDao.account_name,
			DfTradeDao.account_no,
			DfTradeExpanDao.notify_url,
			MerchantDao.secret_key
		).filter(DfTradeDao.order_no == m_args['order_no'])
		dfam = dfam.outerjoin(DfTradeExpanDao,DfTradeDao.order_no == DfTradeExpanDao.order_no)
		dfam = dfam.outerjoin(MerchantDao, MerchantDao.code == DfTradeDao.mer_code)
		dfam = dfam.first()
		if am is not None:
			if am.dongjie_amount is None:
				am_dongjie_amount = 0
			else:
				am_dongjie_amount = am.dongjie_amount
			if dfam.amount is None:
				dfam_amount = 0
			else:
				dfam_amount = dfam.amount
			ams['dongjie_amount'] = am_dongjie_amount - dfam_amount
		try:
			MerchantDao.query.filter(MerchantDao.code == m_args['mer_code']).update(ams)

			DfTradeAgentsDao.query.filter(DfTradeAgentsDao.order_no == m_args['order_no']).update(args)

			DfTradeDao.query.filter(DfTradeDao.order_no == m_args['order_no']).update(args)

			# db.session.commit()
			# db.session.expunge()
			result = []
			result.append({
				'order_no': dfam.order_no,
				'org_order_no': dfam.org_order_no,
				'mer_code': dfam.mer_code,
				'amount': str(dfam.amount),
				'action_time': dfam.action_time,
				'audit_time': dfam.audit_time,
				'sxf': str(dfam.sxf),
				'account_name': dfam.account_name,
				'account_no': dfam.account_no,
				'notify_url': dfam.notify_url,
				'secret_key': dfam.secret_key,
				'state': args['state']
			})
			self.cash_notify_result(result[0])
		except Exception as e:
			db.session.rollback()
			db.session.remove()
			current_app.logger.exception(e)
			return {
				'success': False,
				'error_code': 8001,
				'error_msg': '代付失败'
			}


	def update_remove(self, data_args):
		args = {}
		das = {}
		args['mer_code'] = data_args['mchntCd']
		args['bankCd'] = data_args['bankCd']
		args['order_no'] = data_args['mchntPayforSsn']
		args['account_name'] = data_args['cardName']
		args['account_no'] = data_args['cardNo']
		if data_args['destAmount']  is None:
			data_args['destAmount'] = 0
		args['amount'] = data_args['destAmount'] / 100
		args['action_time'] = int(time.time())
		args['sign'] = data_args['sign']
		args['state'] = 1
		args['state_code'] = data_args['state_code']
		das['amount'] = self.context_merchart.amount
		das['dongjie_amount'] = self.context_merchart.dongjie_amount
		das['code'] = self.context_merchart.code
		try:
			dao = DfTradeAgentsDao(**args)
			MerchantDao.query.filter(MerchantDao.code == das['code']).update(das)
			db.session.add(dao)
			db.session.commit()
		except Exception as e:
			db.session.rollback()
			db.session.remove()
			current_app.logger.exception(e)
			return {
				'success': False,
				'error_code': 8001,
				'error_msg': '代付失败'
			}

	# 回调上游的函数
	def cash_notify_result(self,result):
		secret_key = result.pop('secret_key')
		m_str = self.credit_sign(result,secret_key)
		m_sign = self.get_sign(m_str)
		result['sign'] = m_sign
		res = json.loads(self.cash_post(result, result['notify_url']))


	# 生成加密字符串
	def credit_sign(self,m_args,select_key):
		m_str = ''
		for k in sorted(m_args):
			if m_args[k] is not None:
				m_str += '%s=%s&' % (k, m_args[k])
		m_str = m_str[:-1]
		m_str = m_str + select_key
		return m_str

	# 计算手续费总额
	def calculation_amount_sum(self, mer_code, amount):
		result = WOlinetrideService.calculation_amount_zuida(mer_code,amount)
		sxf = 0
		for res in result:
			sxf_g = decimal.Decimal(str(res['sxf_g']))
			sxf_q = decimal.Decimal(str(res['sxf']))
			am = sxf_g + sxf_q
			sxf += am
		# sxf = float('%.3f' % keep_two_del(sxf))
		agentpayQuerylogger.info('代理手续费总额%s'%sxf)
		return sxf

	# 计算手续费
	@staticmethod
	def calculation_amount(mer_code,amount):
		agentpayQuerylogger.info("计算手续费 . 代付商户 %s , 代付金额 %s "%(mer_code,amount))
		res = db.session.query(DfAgentRate.id.label('id'),
							DfAgentRate.agent_code.label('agent_code'),
							DfAgentRate.agent_name.label('agent_name'),
							DfAgentRate.mer_code.label('mer_code'),
							DfAgentRate.rate_prop.label('rate_prop'),
							DfAgentRate.rate_amount.label('rate_amount'),
							DfAgentRate.mer_username.label('mer_username')
							,MerchantDao.state).filter(MerchantDao.code == DfAgentRate.agent_code , MerchantDao.state == 1 ,DfAgentRate.mer_code == mer_code,).all()
		asm = db.session.query(func.sum(DfTradeDao.amount)).filter(and_(DfTradeDao.mer_code == mer_code,DfTradeDao.state == 2)).scalar()
		agentpayQuerylogger.info("商户当前总成交  :  %s"%(asm))
		if asm is None:
			asm = 0
		asm = asm + amount
		rs = {}
		rs_g = {}
		rs_name = {}
		res_r = []
		for i in res:
			yhjeDict = {}
			yhLists = []
			for args in i.rate_amount:
				yhLists.append(args)
			yhLists.sort(key=lambda x: float(x["ratelower"]))
			rs['%s' % i.agent_code] = yhLists
			rs_g['%s' % i.agent_code] = i.rate_prop
			rs_name['%s' % i.agent_code] = i.agent_name
			res_r.append(i.agent_code)
		sxf_sum = 0
		result = []
		for i in res_r:
			res_di = {}
			rate = rs[i]
			agent_name = rs_name[i]
			# rate_g = float('%.3f' % rs_g[i])
			rate_g = rs_g[i]
			sxf_on = 0
			# sxf_g = decimal.Decimal(str(res['rate_g']))
			sxf_g = amount * rate_g
			agentpayQuerylogger.info('代理%s的固定手续费%s' % (i, sxf_g))
			res_di['agents_code'] = i
			res_di['agents_name'] = agent_name
			res_di['sxf_g'] = str(formatDecimal_two(sxf_g))
			for j in rate:
				sxf = 0
				res_di['sxf'] = str(formatDecimal_two(sxf))
				if j['ratelower'] != '' and j['rateupper'] != '':
					if asm >= j['ratelower'] and asm < j['rateupper']:
						sxf += j['amount']
						res_di['sxf'] = str(formatDecimal_two(sxf))
						agentpayQuerylogger.info('代理%s的手续费%s' % (i, sxf))
						break
				elif not j['ratelower'] and j['rateupper'] != '':
					pass
				elif j['ratelower'] != '' and not j['rateupper']:
					if asm >= j['ratelower']:
						sxf += j['amount']
						res_di['sxf'] = str(formatDecimal_two(sxf))
						agentpayQuerylogger.info('代理%s的手续费%s' % (i, sxf))
						break
				else:
					sxf_on += sxf
			result.append(res_di)
			sxf = decimal.Decimal(str(sxf))
			sxf_sum += sxf + sxf_g
		agentpayQuerylogger.info('代付总手续费%s' % sxf_sum)
		return result


	# 根据最大区间费率计算手续费
	@staticmethod
	def calculation_amount_zuida(mer_code,amount):
		res = db.session.query(DfAgentRate.id.label('id'),
							DfAgentRate.agent_code.label('agent_code'),
							DfAgentRate.agent_name.label('agent_name'),
							DfAgentRate.mer_code.label('mer_code'),
							DfAgentRate.rate_prop.label('rate_prop'),
							DfAgentRate.rate_amount.label('rate_amount'),
							DfAgentRate.mer_username.label('mer_username')
							,MerchantDao.state).filter(MerchantDao.code == DfAgentRate.agent_code , MerchantDao.state == 1 ,DfAgentRate.mer_code == mer_code,).all()
		asm = db.session.query(func.sum(DfTradeDao.amount)).filter(
			and_(DfTradeDao.mer_code == mer_code, DfTradeDao.state == 2)).scalar()
		if asm is None:
			asm = 0
		asm = asm + amount
		rs = {}
		rs_g = {}
		rs_name = {}
		res_r = []
		for i in res:
			yhjeDict = {}
			yhLists = []
			# 根据存款金额进行排序
			for args in i.rate_amount:
				yhLists.append(args)
			yhLists.sort(key=lambda x: float(x["amount"]))
			yhLists.reverse()
			rs['%s' % i.agent_code] = yhLists
			rs_g['%s' % i.agent_code] = i.rate_prop
			rs_name['%s' % i.agent_code] = i.agent_name
			res_r.append(i.agent_code)
		sxf_sum = 0
		result = []
		for i in res_r:
			res_di = {}
			if asm is not None:
				asm = float('%.3f' % asm)
			rate = rs[i]
			agent_name = rs_name[i]
			# rate_g = float('%.3f' % rs_g[i])
			rate_g = rs_g[i]
			sxf_on = 0
			# sxf_g = decimal.Decimal(str(res['rate_g']))
			sxf_g = amount * rate_g
			res_di['agents_code'] = i
			res_di['agents_name'] = agent_name
			res_di['sxf_g'] = sxf_g
			for j in rate:
				sxf = 0
				sxf += j['amount']
				res_di['sxf'] = str(formatDecimal_two(sxf))
				break
			result.append(res_di)
			sxf = decimal.Decimal(str(sxf))
			sxf_sum += sxf + sxf_g
			agentpayQuerylogger.info('返回字段:%s' % result)
			agentpayQuerylogger.info('代理%s的固定手续费:%s' % (i, sxf_g))
			agentpayQuerylogger.info('代理%s的区间手续费:%s' % (i, sxf))
			agentpayQuerylogger.info('该商户的总成交的订单金额%s' % asm)

		return result