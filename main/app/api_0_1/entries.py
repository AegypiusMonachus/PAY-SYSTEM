from flask import Response
from flask_restful import abort
from app.service.qrcode_service import getQRbyTempCode
import os, json
from flask_restful import Resource, marshal_with, fields
from flask_restful.reqparse import RequestParser
from app.api_0_1.common import *
from app.models.onlinetrades_dao import *
from app.models.merchant_dao import *
from app.api_0_1.utils import *


class OrderEntryAPI(Resource):

	@marshal_with(make_fields({
		'id': fields.Integer,
		'order_number': fields.String,
		'amount': fields.Float,
		'original_state': fields.String,
		'final_state': fields.String,
		'notification_number': fields.Integer,
		'username': fields.String,
		'create_timestamp': fields.DateTime,
		'update_timestamp': fields.DateTime,
	}))
	def get(self):
		parser = RequestParser(trim=True)
		parser.add_argument('trade_order', type=str, required=True, nullable=False)
		parser.add_argument('page', type=int, default=DEFAULT_PAGE)
		parser.add_argument('pageSize', type=int, default=DEFAULT_PAGE_SIZE)
		args = parser.parse_args()
		if not args['trade_order']:
			return {'success': False, "error_msg": "订单编号错误"}

		q1 = db.session.query(OrderEntry).filter(OrderEntry.order_number == args['trade_order'])
		pagination = q1.paginate(args['page'], args['pageSize'], error_out=False)
		result = []
		for entry in pagination.items:
			result.append({
				'id':entry.id,
				'order_number':entry.order_number,
				'amount':float(entry.amount) if entry.amount else None,
				'original_state': entry.original_state,
				'final_state': entry.final_state,
				'notification_number': entry.notification_number if entry.notification_number else None,
				'username': entry.username,
				'create_timestamp': entry.create_timestamp,
				'update_timestamp': entry.update_timestamp,
			})
		return make_response(result, page=pagination.page, pages=pagination.pages, total=pagination.total)


class MerchantEntryAPI(Resource):

	@marshal_with(make_fields({
		'id': fields.Integer,
		'merchant_username': fields.String,
		'type': fields.String,
		'order_number': fields.String,
		'amount': fields.Float,
		'balance': fields.Float,
		'create_timestamp': fields.DateTime,
		'update_timestamp': fields.DateTime,
	}))
	def get(self):
		parser = RequestParser(trim=True)
		parser.add_argument('username', type=str)
		parser.add_argument('type', type=str)
		parser.add_argument('create_timestamp', type=int)
		parser.add_argument('page', type=int, default=DEFAULT_PAGE)
		parser.add_argument('pageSize', type=int, default=DEFAULT_PAGE_SIZE)
		args = parser.parse_args()
		if not args['username']:
			return {'success': False, "error_msg": "商戶名错误"}

		criterion = set()
		if args['username']:
			criterion.add(MerchantEntry.merchant_username == args['username'])
		if args['type']:
			criterion.add(MerchantEntry.type == args['type'])
		if args['create_timestamp']:
			criterion.add(MerchantEntry.create_timestamp == args['create_timestamp'])
		q1 = db.session.query(MerchantEntry).filter(*criterion)
		pagination = q1.paginate(args['page'], args['pageSize'], error_out=False)
		result = []
		for entry in pagination.items:
			result.append({
				'id':entry.id,
				'merchant_username':entry.merchant_username,
				'type': entry.type,
				'order_number': entry.order_number,
				'amount':float(entry.amount),
				'balance': float(entry.balance),
				'create_timestamp': entry.create_timestamp,
				'update_timestamp': entry.update_timestamp,
			})
		return make_response(result, page=pagination.page, pages=pagination.pages, total=pagination.total)