import time
from decimal import Decimal

from . import db
from .merchant_dao import MerchantDao, MerchantEntry


class OnlinetradesDao(db.Model):
	__tablename__ = 'tb_onlinetrade'

	id = db.Column(db.Integer, primary_key=True)
	order_no = db.Column(db.String)
	org_order_no = db.Column(db.String)
	bank_order_no = db.Column(db.String)
	qr_code = db.Column(db.String)
	amount = db.Column(db.Numeric, default=0)
	discount_amount = db.Column(db.Numeric, default=0)
	real_amount = db.Column(db.Numeric, default=0)
	bank_amount = db.Column(db.Numeric, default=0)
	action_time = db.Column(db.Integer)
	mer_code = db.Column(db.String)
	user_name = db.Column(db.String)
	pay_type = db.Column(db.Integer)
	cost_service = db.Column(db.Numeric)
	cost_agent = db.Column(db.Numeric)
	audit_time = db.Column(db.Integer)
	state = db.Column(db.Integer)
	remark = db.Column(db.String)
	mer_ip = db.Column(db.String)
	match_type = db.Column(db.Integer)
	drawee = db.Column(db.String)
	real_cost_service = db.Column(db.Numeric, nullable=False)
	real_cost_agent = db.Column(db.Numeric, nullable=False)

	entries = db.relationship('OrderEntry', backref='order', lazy='dynamic')

	def get_cost(self, actual_amount):
		merchant = MerchantDao.select_one_by_username(self.user_name)
		merchant_cost = actual_amount * merchant.get_rate(str(self.pay_type)) / 100

		parent_cost = Decimal(0)
		if merchant.has_parent():
			parent = merchant.get_parent()
			if not parent.has_parent():
				parent_cost = actual_amount * parent.get_rate(str(self.pay_type)) / 100
				parent_cost = merchant_cost - parent_cost

		self.real_cost_service = merchant_cost
		self.real_cost_agent = parent_cost

	def is_created(self):
		return self.state == 1

	def is_finished(self):
		return self.state == 2

	def is_canceled(self):
		return self.state == 3

	def is_confirmed(self):
		return self.state == 4

	def set_finished_manually(self, notification):
		self.state = 2
		self.match_type = 1
		self.audit_time = int(time.time())
		self.bank_amount = notification.amount

		if (self.amount - self.discount_amount) == notification.amount:
			self.get_cost(self.amount)
		else:
			self.get_cost(notification.amount)

	def set_finished_automatically(self):
		self.state = 2
		self.match_type = 1

	def set_canceled(self):
		self.state = 3

	def set_confirmed(self):
		self.state = 4

	@staticmethod
	def select_all(criterion=None):
		if not criterion:
			return OnlinetradesDao.query.all()
		return OnlinetradesDao.query.filter(*criterion).all()

	@staticmethod
	def select_all_unfinished():
		criterion = set()
		criterion.add(OnlinetradesDao.state == 1)
		return OnlinetradesDao.select_all(criterion)

	@staticmethod
	def select_one(criterion=None):
		if not criterion:
			return OnlinetradesDao.query.first()
		return OnlinetradesDao.query.filter(*criterion).first()

	@staticmethod
	def select_one_by_id(id):
		criterion = set()
		criterion.add(OnlinetradesDao.id == id)
		return OnlinetradesDao.select_one(criterion)

	@staticmethod
	def select_one_by_number(number):
		criterion = set()
		criterion.add(OnlinetradesDao.order_no == number)
		return OnlinetradesDao.select_one(criterion)

	@staticmethod
	def select_one_unfinished_by_id(id):
		criterion = set()
		criterion.add(OnlinetradesDao.id == id)
		criterion.add(OnlinetradesDao.state == 1)
		return OnlinetradesDao.select_one(criterion)

	@staticmethod
	def select_one_unfinished_by_number(number):
		criterion = set()
		criterion.add(OnlinetradesDao.order_no == number)
		criterion.add(OnlinetradesDao.state == 1)
		return OnlinetradesDao.select_one(criterion)

	from threading import RLock
	lock = RLock()

	@staticmethod
	def cancel(order):
		if not order:
			return False

		with OnlinetradesDao.lock:
			order.state = 3
			order.audit_time = int(time.time())
			try:
				db.session.add(order)
				db.session.commit()
			except:
				db.session.rollback()
				db.session.remove()
				return False

			from app.extensions import code_manager
			code_manager.cancel(order.qr_code, order.amount, order.discount_amount)
			return True

	@staticmethod
	def finish(order, actual_amount=None):
		if not order:
			return False

		with OnlinetradesDao.lock:
			order.state = 2
			if actual_amount is not None:
				order.match_type = 1
				order.bank_amount = actual_amount
			else:
				order.match_type = 2
				order.bank_amount = order.real_amount
			try:
				db.session.add(order)
				db.session.commit()
			except:
				db.session.rollback()
				db.session.remove()
				return False

			from app.extensions import code_manager
			if actual_amount is not None:
				code_manager.finish(order.qr_code, order.amount, order.discount_amount, order.real_amount)
			else:
				code_manager.finish(order.qr_code, order.amount, order.discount_amount)
			return True


class OrderEntry(db.Model):
	__tablename__ = 'tb_order_entry'

	id = db.Column(db.Integer, primary_key=True)
	order_number = db.Column(db.String, db.ForeignKey('tb_onlinetrade.order_no'), nullable=False)
	original_state = db.Column(db.String, nullable=False)
	final_state = db.Column(db.String, nullable=False)
	amount = db.Column(db.Numeric)
	notification_number = db.Column(db.String)
	username = db.Column(db.String)
	create_timestamp = db.Column(db.DateTime)
	update_timestamp = db.Column(db.DateTime)

	@staticmethod
	def select_all(criterion=None):
		if not criterion:
			return OrderEntry.query.order_by(OrderEntry.create_timestamp.desc()).all()
		return OrderEntry.query.filter(*criterion).order_by(OrderEntry.create_timestamp.desc()).all()

	@staticmethod
	def select_all_by_order(order):
		criterion = set()
		criterion.add(OrderEntry.order_number == order.order_no)
		return OrderEntry.select_all(criterion)

	@staticmethod
	def select_last_one(criterion=None):
		if not criterion:
			return OrderEntry.query.order_by(OrderEntry.create_timestamp.desc()).first()
		return OrderEntry.query.filter(*criterion).order_by(OrderEntry.create_timestamp.desc()).first()

	@staticmethod
	def select_last_one_by_order(order):
		criterion = set()
		criterion.add(OrderEntry.order_number == order.order_no)
		return OrderEntry.select_last_one(criterion)

	@staticmethod
	def insert_one_created_to_canceled(order):
		if not order.is_created():
			return False

		entry = OrderEntry(order_number=order.order_no,
			original_state='CERATED', final_state='CANCELED')
		order.set_canceled()
		try:
			db.session.add(entry)
			db.session.commit()
			return True
		except:
			db.session.rollback()
			db.session.remove()
		return False

	@staticmethod
	def insert_one_created_to_finished_automatically(order, notification):
		if not order.is_created():
			return False

		entry = OrderEntry(order_number=order.order_no, notification_number=notification.order_no,
			original_state='CERATED', final_state='FINISHED MANUALLY')
		order.set_finished_automatically()
		try:
			db.session.add(entry)
			db.session.add(order)
			db.session.commit()
			return True
		except:
			db.session.rollback()
			db.session.remove()
		return False

	@staticmethod
	def insert_one_created_to_finished_manually(order, notification, username):
		if not order.is_created():
			return False

		entry = OrderEntry(order_number=order.order_no, notification_number=notification.order_no, username=username,
			original_state='CERATED', final_state='FINISHED MANUALLY')
		order.set_finished_manually(notification)
		notification.set_finished()
		try:
			db.session.add(entry)
			db.session.add(order)
			db.session.add(notification)
			db.session.commit()

			merchant = MerchantDao.select_one_by_username(order.user_name)
			if (order.amount - order.discount_amount) == notification.amount:
				MerchantEntry.insert_one_income_direct(merchant, order, order.amount - order.real_cost_service)
			else:
				MerchantEntry.insert_one_income_direct(merchant, order, notification.amount - order.real_cost_service)
			if order.real_cost_agent:
				MerchantEntry.insert_one_income_indirect(merchant.get_parent(), order, order.real_cost_agent)

			from app.extensions import code_manager
			code_manager.finish(order.qr_code, order.amount, order.discount_amount, notification.amount)
			return True
		except:
			db.session.rollback()
			db.session.remove()
		return False

	@staticmethod
	def insert_one_canceled_to_confirmed(order, notification, username):
		if not order.is_canceled():
			return False

		entry = OrderEntry(order_number=order.order_no, notification_number=notification.order_no, username=username,
			original_state='CANCELED', final_state='CONFIRMED')
		order.set_confirmed()
		try:
			db.session.add(entry)
			db.session.add(order)
			db.session.commit()
			return True
		except:
			db.session.rollback()
			db.session.remove()
		return False

	@staticmethod
	def insert_one_confirmed_to_canceled(order, username):
		if not order.is_confirmed():
			return False

		entry = OrderEntry(order_number=order.order_no, username=username,
			original_state='CONFIRMED', final_state='CANCELED')
		order.set_canceled()
		try:
			db.session.add(entry)
			db.session.add(order)
			db.session.commit()
			return True
		except:
			db.session.rollback()
			db.session.remove()
		return False

	@staticmethod
	def insert_one_confirmed_to_finished_manually(order, notification, username):
		if not order.is_confirmed():
			return False

		last_entry = OrderEntry.select_last_one_by_order(order)
		if not last_entry:
			return False
		if last_entry.final_state != 'CONFIRMED':
			return False
		if last_entry.notification_number != notification.order_no:
			return False
		if last_entry.username == username:
			return False

		entry = OrderEntry(order_number=order.order_no, notification_number=notification.order_no, username=username,
			original_state='CONFIRMED', final_state='FINISHED MANUALLY')
		order.set_finished_manually(notification)
		notification.set_finished()
		try:
			db.session.add(entry)
			db.session.add(order)
			db.session.add(notification)
			db.session.commit()

			merchant = MerchantDao.select_one_by_username(order.user_name)
			if (order.amount - order.discount_amount) == notification.amount:
				MerchantEntry.insert_one_income_direct(merchant, order, order.amount - order.real_cost_service)
			else:
				MerchantEntry.insert_one_income_direct(merchant, order, notification.amount - order.real_cost_service)
			if order.real_cost_agent:
				MerchantEntry.insert_one_income_indirect(merchant.get_parent(), order, order.real_cost_agent)

			from app.extensions import code_manager
			code_manager.finish2(order.qr_code, order.amount, order.discount_amount, notification.amount)

			return True
		except:
			db.session.rollback()
			db.session.remove()
			return False


class OnlinetradesExpansion(db.Model):
	__tablename__ = 'tb_onlinetrade_expansion'

	id = db.Column(db.Integer, primary_key=True)
	org_order_no = db.Column(db.String)
	order_no = db.Column(db.String)
	mer_notify_url = db.Column(db.String)
	expansion_data = db.Column(db.String)
	temp_code = db.Column(db.String)


class OnlinetradesDatilsDao(db.Model):
	__tablename__ = 'tb_onlinetrade_detail'

	id = db.Column(db.Integer, primary_key=True)
	order_no = db.Column(db.String)
	org_order_no = db.Column(db.String)
	action_time = db.Column(db.Integer)
	state = db.Column(db.Integer)
