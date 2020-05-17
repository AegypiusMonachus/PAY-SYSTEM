from flask_restful import Resource
from app.service.df_merchant_recharge_service import (get_df_recharge_bank,insert_df_merchnt_recharge)
from flask import g
from flask_restful.reqparse import RequestParser
from app.common import formatDecimal

class DfRechargeBankAPI(Resource):
	def get(self):
		res = get_df_recharge_bank()
		if res == None:
			return {'success': False,"errorMsg":"数据错误","errorCode":3001} 
		else:
			return {'success': True,"data":res}
		
class DfMerchantRechargeAPI(Resource):
	def post(self):
		parserpost = RequestParser(trim=True)
		parserpost.add_argument('df_bank_id', type=int)
		parserpost.add_argument('amount', type=str)
		parserpost.add_argument('account_no', type=str)
		parserpost.add_argument('account_name', type=str)
		parserpost.add_argument('df_bank_name', type=str)
		m_args = parserpost.parse_args(strict=True)
		if g.current_member:
			m_args['username'] = g.current_member.username
			m_args['amount'] = formatDecimal(m_args['amount'])
			m_args['state'] = 1
			return insert_df_merchnt_recharge(m_args)
		else:
			return {"success": False, "errorCode": 9999}
			
			
			
			
			