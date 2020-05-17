from flask import Response
from flask_restful import abort
from app.service.qrcode_service import getQRbyTempCode
import os, json
from flask_restful import Resource, marshal_with, fields
from flask_restful.reqparse import RequestParser
from app.api_0_1.common import *
from app.models.onlinetrades_dao import *
from app.models.bank_trade_dao import BankTradeDao


class TradesBankAPI(Resource):

	@marshal_with(make_fields({
		'id': fields.Integer,
		'order_no': fields.String,
		'amount': fields.Float,
		'qr_code': fields.String,
		'action_time': fields.Integer,
		'pay_time': fields.Integer,
		'state': fields.Integer,
	}))
	def get(self):
		parser = RequestParser(trim=True)
		parser.add_argument('trade_order', type=str, required=True, nullable=False)
		args = parser.parse_args()
		if not args['trade_order']:
			return {'success': False, "error_msg": "订单编号错误"}

		onlineTrade = OnlinetradesDao.select_one_by_number(args['trade_order'])
		bankTrades = BankTradeDao.select_all_unfinished_by_code(onlineTrade.qr_code)
		result = []
		for bankTrade in bankTrades:
			result.append({
				'id':bankTrade.id,
				'order_no':bankTrade.order_no,
				'amount':float(bankTrade.amount),
				'qr_code': bankTrade.qr_code,
				'action_time': bankTrade.action_time,
				'pay_time': bankTrade.pay_time,
				'state': bankTrade.state
			})

		return make_response(result)

