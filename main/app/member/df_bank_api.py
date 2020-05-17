from flask_restful import Resource
from app.agentspay.parsers.df_bank_parsers import dfbankparser,dfbankpostparser
from app.models.df_bank_dao import DfBanks
from flask import g
from app.service.df_bank_services import DfBankService


class DfBank(Resource):
	def get(self):
		m_args = dfbankparser.parse_args(strict=True)
		critern = set()
		if g.current_member:
			username = g.current_member.username
			critern.add(DfBanks.user_name == username)
		else:
			return {"success": False, "error_code": 999}
		if 'bankId' in m_args:
			if m_args['bankId'] is not None:
				critern.add(DfBanks.bank_id == m_args['bankId'])

		res = DfBankService().get_bank(critern)
		result = []
		for i in res:
			result.append({
				'id':i.id,
				'user_name': i.user_name,
				'bank_code': i.bank_code,
				'bank_number': i.bank_number,
				'name': i.name
			})

	def post(self):
		m_args = dfbankpostparser.parse_args(strict=True)
		critern = set()
		# if g.current_member:
		# 	m_args['username'] = g.current_member.username
		# else:
		# 	return {"success": False, "error_code": 999}
		m_args['username'] = '500w'
		res = DfBankService().insert_bank(m_args)