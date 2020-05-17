from decimal import Decimal

from . import db
from .refulation_dao import RefulationDao


class MerchantDao(db.Model):
	__tablename__ = 'tb_merchant'
	id = db.Column(db.Integer, primary_key=True)
	code = db.Column(db.String)
	username = db.Column(db.String)
	password = db.Column(db.String)
	type = db.Column(db.Integer)
	parent_code = db.Column(db.String)
	parent_name = db.Column(db.String)
	rate = db.Column(db.JSON)
	secret_key = db.Column(db.String)
	salt = db.Column(db.Integer)
	amount = db.Column(db.Numeric, default=0)
	dongjie_amount = db.Column(db.Numeric)
	real_money = db.Column('real_amount', db.Numeric, default=0)
	level = db.Column(db.Integer)
	state = db.Column(db.Integer, default=1)
	term_of_validity = db.Column(db.Integer)
	default_level = db.Column(db.Integer)
	actionTime = db.Column(db.Integer)
	default_agents = db.Column(db.Integer, default=0)
	wrdraw_amount = db.Column(db.Numeric, default=0)
	entries = db.relationship('MerchantEntry', backref='merchant', lazy='dynamic')

	def get_rate(self, type):
		if type not in self.rate:
			return None
		rate = Decimal(self.rate.get(type, 0))
		return rate.quantize(Decimal('1.000'))

	def get_parent(self):
		return MerchantDao.select_one_by_username(self.parent_name)

	def has_parent(self):
		if not self.parent_name:
			return False
		default = RefulationDao.query.first()
		if self.parent_name == default.agents:
			return False
		return True

	@staticmethod
	def select_all(criterion=None):
		if not criterion:
			return MerchantDao.query.all()
		return MerchantDao.query.filter(*criterion).all()

	@staticmethod
	def select_one(criterion=None):
		if not criterion:
			return MerchantDao.query.first()
		return MerchantDao.query.filter(*criterion).first()

	@staticmethod
	def select_one_by_username(username):
		criterion = set()
		criterion.add(MerchantDao.username == username)
		return MerchantDao.select_one(criterion)

	def get_data(self, mer_code):
		res = db.session.query(MerchantDao).filter(MerchantDao.code == mer_code).first()
		return res


class MerchantEntry(db.Model):
	__tablename__ = 'tb_merchant_entry'

	id = db.Column(db.Integer, primary_key=True)
	type = db.Column(db.String)
	merchant_username = db.Column(db.String, db.ForeignKey('tb_merchant.username'))
	order_number = db.Column(db.String)
	amount = db.Column(db.Numeric)
	balance = db.Column(db.Numeric)
	create_timestamp = db.Column(db.DateTime)
	update_timestamp = db.Column(db.DateTime)

	@staticmethod
	def select_all(criterion=None):
		if not criterion:
			return MerchantEntry.query.all()
		return MerchantEntry.query.filter(*criterion).all()

	@staticmethod
	def select_one(criterion=None):
		if not criterion:
			return MerchantEntry.query.first()
		return MerchantEntry.query.filter(*criterion).first()

	@staticmethod
	def select_all_by_merchant_username_and_order_number(merchant_username=None, order_number=None):
		criterion = set()
		if merchant_username:
			criterion.add(MerchantEntry.merchant_username == merchant_username)
		if order_number:
			criterion.add(MerchantEntry.order_number == order_number)
		return MerchantEntry.select_all(criterion)

	@staticmethod
	def insert_one_income_direct(merchant, order, amount):
		entry = MerchantEntry()
		entry.type = 'INCOME DIRECT'
		entry.merchant_username = merchant.username
		entry.balance = merchant.amount
		entry.order_number = order.order_no
		entry.amount = amount

		merchant.amount += amount
		try:
			db.session.add(entry)
			db.session.add(merchant)
			db.session.commit()
		except:
			db.session.rollback()
			db.session.remove()

	@staticmethod
	def insert_one_income_indirect(merchant, order, amount):
		entry = MerchantEntry()
		entry.type = 'INCOME INDIRECT'
		entry.merchant_username = merchant.username
		entry.balance = merchant.amount
		entry.order_number = order.order_no
		entry.amount = amount

		merchant.amount += amount
		try:
			db.session.add(entry)
			db.session.add(merchant)
			db.session.commit()
		except:
			db.session.rollback()
			db.session.remove()


class MerchantBank(db.Model):
	__tablename__ = 'tb_merchant_bank'

	id = db.Column(db.Integer, primary_key=True)
	code = db.Column('mer_code',db.String)
	bankNumber = db.Column('bank_id',db.String)
	numbers = db.Column('account',db.String)
	bankname = db.Column('payee',db.Integer)


class MerchantInfo(db.Model):
	__tablename__ = 'tb_merchant_info'

	id = db.Column(db.Integer, primary_key=True)
	code = db.Column('mer_code',db.String)
	name = db.Column(db.String)
	telephone = db.Column(db.String)
	mobilephone = db.Column(db.Integer)
	email = db.Column(db.String)
	remark = db.Column(db.String)


class PayType(db.Model):
	__tablename__ = 'tb_config_dic'

	id = db.Column(db.Integer, primary_key=True)
	code = db.Column(db.Integer)
	type = db.Column(db.Integer)
	name = db.Column(db.String)
	remark = db.Column(db.String)
