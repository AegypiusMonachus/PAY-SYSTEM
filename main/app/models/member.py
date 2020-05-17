from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash

from . import db


class Member(db.Model):
	__tablename__ = 'tb_members'

	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String, unique=True)
	password_hash = db.Column(db.String)

	@property
	def password(self):
		raise AttributeError

	@password.setter
	def password(self, password):
		self.password_hash = generate_password_hash(password)

	@staticmethod
	def verify_password(member, password):
		return check_password_hash(member.password_hash, password)

	@staticmethod
	def generate_token(member):
		return current_app.serializer.dumps({'id': member.id}).decode()

	@staticmethod
	def verify_token(token):
		try:
			return Member.query.get(current_app.serializer.loads(token).get('id'))
		except:
			return None
