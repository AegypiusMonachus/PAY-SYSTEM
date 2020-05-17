from . import db


class Qrcode(db.Model):
	__tablename__ = 'tb_qrcode'

	id = db.Column(db.Integer, primary_key=True)
	code = db.Column(db.String)
	qr_image = db.Column(db.String)
	bank_id = db.Column(db.Integer)
	lower_amount = db.Column(db.Numeric)
	upper_amount = db.Column(db.Numeric)
	state = db.Column(db.Integer, default=1)
	levels = db.Column(db.JSON)
	remark = db.Column(db.String)
	rate = db.Column(db.JSON)
	type = db.Column(db.Integer)
	regulation_id = db.Column(db.Integer)
	ori_type = db.Column(db.Integer)
	names = db.Column('name', db.String)
	receive_member = db.Column(db.String)
	bank_account = db.Column(db.String)
	phone_number = db.Column(db.String)
	valid_time = db.Column(db.Integer)
	create_time = db.Column(db.Integer)
	new_qrcode = db.Column(db.String)

	@staticmethod
	def select_all(criterion=None):
		if not criterion:
			return Qrcode.query.all()
		return Qrcode.query.filter(*criterion).all()

	@staticmethod
	def select_all_enabled():
		criterion = set()
		criterion.add(Qrcode.state == 1)
		return Qrcode.select_all(criterion)

	@staticmethod
	def select_all_by_names(names):
		criterion = set()
		criterion.add(Qrcode.names.in_(names))
		return Qrcode.select_all(criterion)

	@staticmethod
	def select_all_by_codes(codes):
		criterion = set()
		criterion.add(Qrcode.code.in_(codes))
		return Qrcode.select_all(criterion)

	@staticmethod
	def select_one(criterion=None):
		if not criterion:
			return Qrcode.query.first()
		return Qrcode.query.filter(*criterion).first()

	@staticmethod
	def select_one_by_name(name):
		criterion = set()
		criterion.add(Qrcode.names == name)
		return Qrcode.select_one(criterion)

	@staticmethod
	def select_one_by_code(code):
		criterion = set()
		criterion.add(Qrcode.code == code)
		return Qrcode.select_one(criterion)