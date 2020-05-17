from flask_restful import Resource
from app.service.w_onlinetride_service import WOlinetrideService
from app.agentspay.parsers.cash_withdrawal_parsers import dfcashwithdrawalparser
from app.service.df_trade_query_service import DFQueryDetailService
from flask_restful.reqparse import RequestParser

class AgentspayApi(Resource):
	def post(self):
		m_args = dfcashwithdrawalparser.parse_args(strict=True)
		print(m_args)
		res = WOlinetrideService()
		args = res.receive_withdrawal(m_args)
		if args is not 	None:
			if args['success'] == True:
				return args
			else:
				return args
			
			

class AgentspayQueryApi(Resource):
	def post(self):
		m_result  ={}
		parserpost = RequestParser(trim=True)
		parserpost.add_argument('mer_code', type=str)
		parserpost.add_argument('org_order_no', type=str)
		parserpost.add_argument('sign', type=str)
		m_args = parserpost.parse_args(strict=True)
		service = DFQueryDetailService(m_args)
		res = service.queryDetail()
		if service.success == True:
			m_result['data'] = res
			m_result['success'] = True
		else :
			m_result['success'] = False
			m_result['error_msg'] = service.error_msg
			m_result['error_code'] = service.error_code
		return m_result
