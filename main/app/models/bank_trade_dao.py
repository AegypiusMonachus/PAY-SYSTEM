import time

from . import db


class BankTradeDao(db.Model):
	__tablename__ = 'tb_banktrade'

	id = db.Column(db.Integer, primary_key=True)
	order_no = db.Column(db.String)
	amount = db.Column(db.Numeric, default=0)
	qr_code = db.Column(db.String)
	action_time = db.Column(db.Integer)
	expansion_data = db.Column(db.String)
	pay_time = db.Column(db.Integer)
	state = db.Column(db.Integer, default=1)
	audit_time = db.Column(db.Integer)

	def is_finished(self):
		return self.state == 2

	def set_finished(self):
		self.state = 2
		self.audit_time = int(time.time())

	@staticmethod
	def select_all(criterion=None):
		if not criterion:
			return BankTradeDao.query.all()
		return BankTradeDao.query.filter(*criterion).all()

	@staticmethod
	def select_all_finished_by_code(code):
		criterion = set()
		criterion.add(BankTradeDao.qr_code == code)
		criterion.add(BankTradeDao.state == 2)
		return BankTradeDao.select_all(criterion)

	@staticmethod
	def select_all_unfinished_by_code(code):
		criterion = set()
		criterion.add(BankTradeDao.qr_code == code)
		criterion.add(BankTradeDao.state != 2)
		return BankTradeDao.select_all(criterion)

	@staticmethod
	def select_one(criterion=None):
		if not criterion:
			return BankTradeDao.query.first()
		return BankTradeDao.query.filter(*criterion).first()

	@staticmethod
	def select_one_by_id(id):
		return BankTradeDao.query.get(id)

	@staticmethod
	def select_one_by_number(number):
		criterion = set()
		criterion.add(BankTradeDao.order_no == number)
		return BankTradeDao.select_one(criterion)
