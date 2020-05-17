from logging import getLogger
logger = getLogger('flask.app')


from decimal import Decimal
from time import sleep
from datetime import datetime, timedelta
from threading import Thread, RLock

from .models.code import CodeOrder
from .models.transaction_code_dao import Qrcode
from .models.onlinetrades_dao import OnlinetradesDao


class CodeManager:

	@staticmethod
	def format(value):
		if isinstance(value, float):
			value = Decimal.from_float(value)
		if isinstance(value, int) or isinstance(value, str):
			value = Decimal(value)
		if not isinstance(value, Decimal):
			raise ValueError
		value = value.quantize(Decimal('1.000'))
		return value

	@staticmethod
	def get_discount_amount(c):
		discount_amount = Decimal('0.01')
		while discount_amount in c:
			discount_amount += Decimal('0.01')
		c.append(discount_amount)
		c.sort()
		return discount_amount

	@staticmethod
	def n_discount_amount(amount):
		return int(CodeManager.format(amount / 10) / CodeManager.format('0.01'))

	def __init__(self, adapter):
		self.lock = RLock()
		self.adapter = adapter

	def _load_c(self, code, lower_limit, upper_limit):
		self.status[code] = {'lower_limit': lower_limit, 'upper_limit': upper_limit,
			'received': Decimal('0'), 'receivable': Decimal('0'), 'c': {}}

	def _load_o(self, code, status, amount, discount_amount, total_amount, actual_amount):
		if code not in self.status:
			return
		if not actual_amount:
			actual_amount = Decimal('0')
		if status in ['FINISHED']:
			self.status[code]['received'] += actual_amount
		if status in ['ACQUIRED']:
			if not self.status[code]['c'].get(amount):
				self.status[code]['c'][amount] = []
			self.status[code]['c'][amount].append(discount_amount)
			self.status[code]['c'][amount].sort()
			self.status[code]['receivable'] += total_amount

	def refresh(self):
		with self.lock:
			self.status = {}
			for r in self.adapter.select_code():
				self._load_c(**r)
			for r in self.adapter.select_order():
				self._load_o(**r)

	# 选择能够分配随机优惠的资源
	def find_available(self, amount):
		n = CodeManager.n_discount_amount(amount)
		codes = []
		for k, v in self.status.items():
			c = v['c'].get(amount)
			if not c or len(c) < n:
				codes.append(k)
		return codes

	# 选择能够容纳充值金额的资源
	def find_available2(self, amount):
		codes = []
		for k, v in self.status.items():
			if v['lower_limit'] <= amount <= v['upper_limit']:
				codes.append(k)
		return codes

	def find_min_receivable(self, codes):
		result = None
		for code in codes:
			if not result:
				result = code
			if self.status[code]['receivable'] < self.status[result]['receivable']:
				result = code
		return result

	def find_min_received(self, codes):
		result = None
		for code in codes:
			if not result:
				result = code
			if self.status[code]['received'] < self.status[result]['received']:
				result = code
		return result

	def acquire(self, amount):
		amount = self.format(amount)
		with self.lock:
			codes = self.find_available(amount)
			if not codes:
				return '资源超限'
			codes = self.find_available2(amount)
			if not codes:
				return '金额超限'

			code = self.find_min_receivable(codes)
			if not self.status[code]['c'].get(amount):
				self.status[code]['c'][amount] = []

			discount_amount = CodeManager.get_discount_amount(self.status[code]['c'][amount])
			self.status[code]['receivable'] += (amount - discount_amount)
			self.adapter.create_order(code, amount, discount_amount)
			return (code, discount_amount)

	def release(self, code, amount, discount_amount):
		if code not in self.status:
			return
		amount = CodeManager.format(amount)
		discount_amount = CodeManager.format(discount_amount)
		with self.lock:
			if not self.status[code]['c'].get(amount):
				return False
			if discount_amount not in self.status[code]['c'][amount]:
				return False
			self.status[code]['c'][amount].remove(discount_amount)
			if not self.status[code]['c'][amount]:
				del self.status[code]['c'][amount]
			return True

	def cancel(self, code, amount, discount_amount):
		if code not in self.status:
			return
		total_amount = amount - discount_amount
		with self.lock:
			if self.release(code, amount, discount_amount):
				self.status[code]['receivable'] -= total_amount
				self.adapter.cancel_order(code, amount, discount_amount)

	def finish(self, code, amount, discount_amount, actual_amount=None):
		if code not in self.status:
			return
		amount = CodeManager.format(amount)
		discount_amount = CodeManager.format(discount_amount)
		total_amount = amount - discount_amount
		if not actual_amount:
			actual_amount = total_amount
		actual_amount = CodeManager.format(actual_amount)
		with self.lock:
			if self.release(code, amount, discount_amount):
				self.status[code]['receivable'] -= total_amount
				self.status[code]['received'] += actual_amount
				self.adapter.finish_order(code, amount, discount_amount, actual_amount)

	def finish2(self, code, amount, discount_amount, actual_amount=None):
		if code not in self.status:
			return
		amount = CodeManager.format(amount)
		discount_amount = CodeManager.format(discount_amount)
		total_amount = amount - discount_amount
		if not actual_amount:
			actual_amount = total_amount
		actual_amount = CodeManager.format(actual_amount)
		with self.lock:
			self.status[code]['receivable'] -= total_amount
			self.status[code]['received'] += actual_amount

	def get_status(self):
		with self.lock:
			return self.status.copy() if self.status else dict()


class CodeAdapter:
	def create_order(self, code, amount, discount_amount):
		return CodeOrder.create_one(code, amount, discount_amount)

	def cancel_order(self, code, amount, discount_amount):
		return CodeOrder.update_one_acquired_to_canceled(code, amount, discount_amount)

	def finish_order(self, code, amount, discount_amount, actual_amount=None):
		return CodeOrder.update_one_acquired_to_finished(code, amount, discount_amount, actual_amount)

	def select_order(self):
		results = []
		for r in CodeOrder.select_all_acquired_and_finished():
			results.append({
				'code': r.code, 'status': r.status,
				'amount': r.amount, 'discount_amount': r.discount_amount, 'total_amount': r.total_amount,
				'actual_amount': r.actual_amount
			})
		return results

	def select_code(self):
		results = []
		for r in Qrcode.select_all_enabled():
			results.append({'code': r.code, 'lower_limit': r.lower_amount, 'upper_limit': r.upper_amount})
		return results


code_manager = CodeManager(CodeAdapter())
