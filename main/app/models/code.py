from . import db


class CodeOrder(db.Model):
	__tablename__ = 'tb_qrcode_order'

	id = db.Column(db.Integer, primary_key=True)
	code = db.Column(db.String, nullable=False)
	amount = db.Column(db.Numeric, nullable=False)
	discount_amount = db.Column(db.Numeric, nullable=False)
	total_amount = db.Column(db.Numeric, nullable=False)
	actual_amount = db.Column(db.Numeric)
	status = db.Column(db.String, nullable=False, default='ACQUIRED')
	create_time = db.Column('create_timestamp', db.DateTime)
	update_time = db.Column('update_timestamp', db.DateTime)

	@staticmethod
	def create_one(code, amount, discount_amount):
		total_amount = amount - discount_amount

		order = CodeOrder()
		order.code = code
		order.amount = amount
		order.discount_amount = discount_amount
		order.total_amount = total_amount
		try:
			db.session.add(order)
			db.session.commit()
			return order
		except:
			db.session.rollback()
			db.session.remove()
		return None

	@staticmethod
	def select_all(criterion=None):
		if not criterion:
			return CodeOrder.query.all()
		return CodeOrder.query.filter(*criterion).all()

	@staticmethod
	def select_one(criterion=None):
		if not criterion:
			return CodeOrder.query.one()
		return CodeOrder.query.filter(*criterion).one()

	@staticmethod
	def select_one_acquired(code, amount, discount_amount):
		total_amount = amount - discount_amount

		criterion = set()
		criterion.add(CodeOrder.code == code)
		criterion.add(CodeOrder.amount == amount)
		criterion.add(CodeOrder.discount_amount == discount_amount)
		criterion.add(CodeOrder.total_amount == total_amount)
		criterion.add(CodeOrder.status == 'ACQUIRED')
		return CodeOrder.select_one(criterion)

	@staticmethod
	def select_all_acquired_and_finished():
		criterion = set()
		criterion.add(CodeOrder.status.in_(['ACQUIRED', 'FINISHED']))
		return CodeOrder.select_all(criterion)

	@staticmethod
	def update_one_acquired(code, amount, discount_amount, actual_amount, status):
		order = CodeOrder.select_one_acquired(code, amount, discount_amount)
		if not order:
			return None
		order.actual_amount = actual_amount if actual_amount else order.total_amount
		order.status = status
		try:
			db.session.add(order)
			db.session.commit()
			return order
		except:
			db.session.rollback()
			db.session.remove()
		return None

	@staticmethod
	def update_one_acquired_to_canceled(code, amount, discount_amount):
		return CodeOrder.update_one_acquired(code, amount, discount_amount, None, 'CANCELED')

	@staticmethod
	def update_one_acquired_to_finished(code, amount, discount_amount, actual_amount=None):
		return CodeOrder.update_one_acquired(code, amount, discount_amount, actual_amount, 'FINISHED')


relationship_code_label = db.Table('tb_relationship_qrcode_label',
	db.Column('code_id', db.Integer, db.ForeignKey('tb_qrcode.id')),
	db.Column('code_label_id', db.Integer, db.ForeignKey('tb_qrcode_label.id'))
)


class CodeLabel(db.Model):
	__tablename__ = 'tb_qrcode_label'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String, nullable=False)

	codes = db.relationship(
		'Qrcode', secondary=relationship_code_label, backref=db.backref('labels', lazy='dynamic')
	)

	@staticmethod
	def select_all(criterion=None):
		if not criterion:
			return CodeLabel.query.all()
		return CodeLabel.query.filter(*criterion).all()

	@staticmethod
	def select_all_by_names(names):
		criterion = set()
		criterion.add(CodeLabel.name.in_(names))
		return CodeLabel.select_all(criterion)

	@staticmethod
	def select_one(criterion=None):
		if not criterion:
			return CodeLabel.query.first()
		return CodeLabel.query.filter(*criterion).first()

	@staticmethod
	def select_one_by_name(name):
		criterion = set()
		criterion.add(CodeLabel.name == name)
		return CodeLabel.select_one(criterion)

	@staticmethod
	def insert_label(name):
		if CodeLabel.select_one_by_name(name):
			return False
		try:
			db.session.add(CodeLabel(name=name))
			db.session.commit()
			return True
		except:
			db.session.rollback()
			db.session.remove()
			return False

	@staticmethod
	def insert_labels(names):
		try:
			for name in names:
				if not CodeLabel.select_one_by_name(name):
					db.session.add(CodeLabel(name=name))
			db.session.commit()
		except:
			db.session.rollback()
			db.session.remove()

	@staticmethod
	def append_code(label, code):
		if code not in label.codes:
			label.codes.append(code)
		try:
			db.session.commit()
		except:
			db.session.rollback()
			db.session.remove()

	@staticmethod
	def append_codes(labels, codes):
		for label in labels:
			for code in codes:
				if code not in label.codes:
					label.codes.append(code)
		try:
			db.session.commit()
			return True
		except:
			db.session.rollback()
			db.session.remove()
			return False

	@staticmethod
	def remove_code(label, code):
		if code in label.codes:
			label.codes.remove(code)
		try:
			db.session.commit()
		except:
			db.session.rollback()
			db.session.remove()

	@staticmethod
	def remove_codes(label, codes):
		for code in codes:
			if code in label.codes:
				label.codes.remove(code)
		try:
			db.session.commit()
		except:
			db.session.rollback()
			db.session.remove()

	@staticmethod
	def reset_labels(labels, code):
		results = code.labels.all()
		for result in results:
			result.codes.remove(code)
		try:
			db.session.commit()
		except:
			db.session.rollback()
			db.session.remove()
			return False

		if not labels:
			return True

		for label in labels:
			label.codes.append(code)
		try:
			db.session.commit()
			return True
		except:
			db.session.rollback()
			db.session.remove()
			return False
