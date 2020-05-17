from flask_restful import Resource, marshal_with, fields
from flask_restful.reqparse import RequestParser

from app.extensions import order_manager


class Orders(Resource):
	def get(self):
		parser = RequestParser()
		parser.add_argument('order', type=str, required=True)
		args = parser.parse_args(strict=True)

		order_manager.put(args['order'])
		return None
