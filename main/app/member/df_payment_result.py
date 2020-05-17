from flask_restful import Resource
from app.agentspay.parsers.df_payment_resultparsers import dfpaymentresultparser
from app.service.w_onlinetride_service import WOlinetrideService



class PaymentResult(Resource):
	def get(self):
		m_args = dfpaymentresultparser.parse_args(strict=True)
		args = WOlinetrideService().get_send_withdrawal(m_args)
		return args