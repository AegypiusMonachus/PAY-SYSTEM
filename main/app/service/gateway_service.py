import time, json
from app.common import *
from app.models import db
from app.models.merchant_dao import MerchantDao
from app.models.onlinetrades_dao import OnlinetradesDao, OnlinetradesExpansion
from app.models.refulation_dao import RefulationDao
from app.models.transaction_code_dao import Qrcode
from .serviceutils.utils import encrypt_md5
from .merchant_service import getDataByCode
from .onlinetrades_service import getOnlineDateByCountOrderNo
from app.redis.redisConnectionManager import PayRedisManager
from app.extensions import code_manager
from config import Config
from decimal import *
import hashlib
from app.log import paylogger

paytype_list = [1001, 1002, 1005, 1008]


class GatewayService():
	def __init__(self, args):
		self.__context = args
		self.success = True
		self.error_code = None
		self.error_msg = None
		self.__merchantDao = None
		self.__onlinetradeDao = None
		self.__onlinetradeExpansionDao = None
		self.__temp_address = None
		self.sign = None

	def getGateway(self):
		# 1：验证参数
		self.sign = self.__context.pop('sign')
		self.__verifyParam()
		if self.success == False:
			return
		try:
			self.__context['amount'] = keep_two_del(Decimal(self.__context['amount']))
			code_decimal = code_manager.acquire(self.__context['amount'])
			if code_decimal == '金额超限':
				self.error_msg = '金额超限'
				self.error_code = 9050
				self.success = False
				return
			if code_decimal == '资源超限':
				self.error_msg = '通道维护'
				self.error_code = 9020
				self.success = False
				return
			qr_code = code_decimal[0]
			random_decimal = code_decimal[1]
			self.creat_order(qr_code, random_decimal)
			self.creat_address()
			data = self.return_data(qr_code)
		except Exception as e:
			db.session.delete(trade)
			db.session.delete(expansion)
			db.session.commit()
			paylogger.exception(e)
			paylogger.error("生成订单异常")
			self.error_msg = '通道维护'
			self.error_code = 9020
			self.success = False
			return
		try:
			json_str = json.dumps(data)
			redisImpl = PayRedisManager.get_redisImpl()
			redisImpl.set(self.__onlinetradeExpansionDao.temp_code, json_str, Config.DEFAULT_TRADE_TIME)
		except Exception as e:
			code_manager.cancel(qr_code, Decimal.from_float(self.__context['amount']), random_decimal)
			trade = db.session.query(OnlinetradesDao).filter(
				OnlinetradesDao.org_order_no == self.__onlinetradeDao.org_order_no).first()
			expansion = db.session.query(OnlinetradesExpansion).filter(
				OnlinetradesExpansion.org_order_no == self.__onlinetradeDao.org_order_no).first()
			db.session.delete(trade)
			db.session.delete(expansion)
			db.session.commit()
			paylogger.exception(e)
			paylogger.error("生成订单异常")
			self.error_msg = '通道维护'
			self.error_code = 9020
			self.success = False
			return
		del data['ep_time']
		data['real_amount']
		result = {}
		result['success'] = True
		result['data'] = data
		try:
			import requests
			requests.get('http://127.0.0.1:5006/api/0.1/orders', params={'order': data['order_no']}, timeout=2)
			requests.get('http://127.0.0.1:8125/main/payCreate', timeout=2)
		except:
			pass
		return result

	def creat_order(self, qr_code, random_decimal):
		onlinetrade = OnlinetradesDao()
		onlinetradesExpansion = OnlinetradesExpansion()
		onlinetrade.qr_code = qr_code
		onlinetrade.order_no = creat_order_no(self.__context['pay_type'], self.__merchantDao.id)
		onlinetrade.mer_code = self.__context['mer_code']
		onlinetrade.amount = self.__context['amount']
		onlinetrade.discount_amount = random_decimal
		onlinetrade.real_amount = self.__context['amount'] - random_decimal
		onlinetrade.org_order_no = self.__context['org_order_no']
		onlinetrade.pay_type = self.__context['pay_type']
		onlinetrade.cost_agent = self.__cost_agent()
		onlinetrade.cost_service = self.__cost_service()
		onlinetrade.action_time = int(time.time())
		onlinetrade.state = 1
		if self.__context['user_name']:
			onlinetrade.drawee = self.__context['user_name']
		onlinetrade.user_name = self.__merchantDao.username
		if self.__context['remark']:
			onlinetrade.remark = self.__context['remark']
		org = str(onlinetrade.order_no) + str(self.__context['org_order_no'])
		org_no = encrypt_md5(org)
		onlinetradesExpansion.org_order_no = self.__context['org_order_no']
		onlinetradesExpansion.order_no = onlinetrade.order_no
		onlinetradesExpansion.temp_code = org_no
		onlinetradesExpansion.mer_notify_url = self.__context['notify_url']
		order = self.__context
		order['amount'] = float(order['amount'])
		onlinetradesExpansion.expansion_data = json.dumps(order)
		try:
			db.session.add(onlinetrade)
			db.session.add(onlinetradesExpansion)
			db.session.commit()
			self.__onlinetradeDao = onlinetrade
			self.__onlinetradeExpansionDao = onlinetradesExpansion
		except Exception as e:
			code_manager.cancel(qr_code, Decimal.from_float(self.__context['amount']), random_decimal)
			db.session.rollback()
			db.session.remove()
			paylogger.exception(e)
			paylogger.error("生成订单异常")
			raise Exception(e)

	def __verifyParam(self):
		self.__merchantDao = getDataByCode(self.__context['mer_code'])
		if self.__merchantDao == None:
			self.error_code = 9011
			self.error_msg = '商户编号错误'
			self.success = False
			return
		mcount = getOnlineDateByCountOrderNo(self.__context['org_order_no'])
		if mcount != 0:
			self.error_code = 9018
			self.error_msg = '订单号重复'
			self.success = False
			return
		if self.__context['pay_type'] not in paytype_list:
			self.error_code = 9015
			self.error_msg = '支付类型错误'
			self.success = False
			return
		msign = self.__sign()
		if self.sign != msign:
			self.error_code = 9017
			self.error_msg = '签名不正确'
			self.success = False
			return

	def __sign(self):
		paramStr = ''
		keyList = sorted(self.__context.keys(), reverse=False)
		for key in keyList:
			if self.__context[key]:
				paramStr += '%s=%s&' % (key, self.__context[key])
		paramStr = paramStr[:-1]
		print(paramStr)
		md = hashlib.md5()
		md.update((paramStr + self.__merchantDao.secret_key).encode())
		m_sign = md.hexdigest()
		print(m_sign)
		return m_sign

	def __cost_service(self):
		cost_service = 0.0
		Rate = self.__merchantDao.rate
		if Rate and str(self.__context['pay_type']) in Rate:
			if Rate[str(self.__context['pay_type'])] is not None:
				costService = code_manager.format((Rate[str(self.__context['pay_type'])] / 100))
				cost_service = keep_three(self.__context['amount'] * costService)
		return cost_service

	def __cost_agent(self):
		cost_agent = 0.0
		if Config.DEFAULT_AGENT == self.__merchantDao.parent_name or not self.__merchantDao.parent_name:
			cost_agent = 0.0
		elif Config.DEFAULT_AGENT != self.__merchantDao.parent_name:
			parent = db.session.query(MerchantDao).filter(
				MerchantDao.username == self.__merchantDao.parent_name).first()
			parentRate = parent.rate
			Rate = self.__merchantDao.rate
			if parentRate:
				if str(self.__context['pay_type']) in parentRate and str(self.__context['pay_type']) in Rate:
					if Rate[str(self.__context['pay_type'])] >= parentRate[str(self.__context['pay_type'])]:
						costAgent = Rate[str(self.__context['pay_type'])] - parentRate[str(self.__context['pay_type'])]
						costAgent = code_manager.format((costAgent / 100))
						cost_agent = keep_three_del(self.__context['amount'] * costAgent)
		return cost_agent

	def creat_address(self):
		self.__temp_address = Config.PAY_VIEW_URL + self.__onlinetradeExpansionDao.temp_code

	# 返回数据
	def return_data(self,qr_code):
		data = {}
		code_id = db.session.query(Qrcode.id).filter(Qrcode.code == qr_code).first()
		data['code_id'] = code_id[0]
		data['org_order_no'] = self.__onlinetradeDao.org_order_no
		data['order_no'] = self.__onlinetradeDao.order_no
		data['qr_URL'] = self.__temp_address
		data['action_time'] = int(time.time())
		data['ep_time'] = int(time.time()) + Config.PAY_VIEW_TTL
		data['amount'] = str(self.__onlinetradeDao.amount)
		data['real_amount'] = str(self.__onlinetradeDao.real_amount)
		return data
