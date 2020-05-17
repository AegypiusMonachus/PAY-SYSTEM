from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


class Order(db.Model):
	__tablename__ = 'tb_onlinetrade'

	id = db.Column(db.Integer, primary_key=True)
	status = db.Column('state', db.Integer)
	create_timestamp = db.Column(db.DateTime)

	@staticmethod
	def select_all(criterion=None):
		if not criterion:
			return Order.query.all()
		return Order.query.filter(*criterion).all()

	@staticmethod
	def select_all_unfinished():
		criterion = set()
		criterion.add(Order.status == 1)
		return Order.select_all(criterion)
