from flask import request
from flask.views import MethodView
from flask.json import jsonify


class RequestHeader(MethodView):
	def get(self):
		response = {key: value for key, value in request.headers.items()}
		return jsonify(response)


class TestRequest(MethodView):
	def get(self):
		return jsonify({'success': True})
