from flask_restful import Resource
from app.agentspay.parsers.df_amount_parsers import dfamountparser
from app.service.w_onlinetride_service import WOlinetrideService


class DfAmount(Resource):

	def post(self):
		m_args = dfamountparser.parse_args(strict=True)
		if  m_args['mer_code'] is None:
			return {'success': False, "error_code": 9011, "error_msg": "商户编号错误/不能为空"}
		if m_args['org_order_no'] is None:
			return {'success': False, "error_code": 9012, "error_msg": "订单号错误/不能为空"}
		if  m_args['name'] is None:
			return {'success': False, "error_code": 9013, "error_msg": "姓名错误/不能为空"}
		if  m_args['account_number'] is None:
			return {'success': False, "error_code": 9014, "error_msg": "银行卡号错误/不能为空"}
		if  m_args['amount'] is None:
			return {'success': False, "error_code": 9015, "error_msg": "金额错误/不能为空"}
		if  m_args['bankcard'] is None:
			return {'success': False, "error_code": 9016, "error_msg": "银行错误/不能为空"}
		if  m_args['sign'] is None:
			return {'success': False, "error_code": 9018, "error_msg": "签名不能为空"}
		res = WOlinetrideService(m_args).receive_withdrawal(m_args)
		return res