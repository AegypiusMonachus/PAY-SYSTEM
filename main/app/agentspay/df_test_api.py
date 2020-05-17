from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from app.service.w_onlinetride_service import WOlinetrideService
import hashlib,time,random
from flask import request

'''
上游代付交易接口
'''
class TestApi(Resource):
	def post(self):
		dfcashwithdrawalparser = RequestParser(trim=True)
		dfcashwithdrawalparser.add_argument('mer_code', type=str)
		dfcashwithdrawalparser.add_argument('org_order_no', type=str)
		dfcashwithdrawalparser.add_argument('name', type=str)
		dfcashwithdrawalparser.add_argument('account_number', type=str)
		dfcashwithdrawalparser.add_argument('amount', type=str)
		dfcashwithdrawalparser.add_argument('bankcard', type=int)
		dfcashwithdrawalparser.add_argument('action_time', type=int)
		dfcashwithdrawalparser.add_argument('sign', type=str)
		m_args = dfcashwithdrawalparser.parse_args(strict=True)
		service = WOlinetrideService(m_args)
		service = service.receive_withdrawal(m_args)
		print('********************************************************')
		print(service)
		print('********************************************************')
		return service
'''
下游代付交易接口
'''
class DownTestApi(Resource):
	def post(self):
		dfcashwithdrawalparserpost = RequestParser(trim=True)
		dfcashwithdrawalparserpost.add_argument('mchntCd', type=str)
		dfcashwithdrawalparserpost.add_argument('mchntPayforSsn', type=str)
		dfcashwithdrawalparserpost.add_argument('cardName', type=str)
		dfcashwithdrawalparserpost.add_argument('cardNo', type=str)
		dfcashwithdrawalparserpost.add_argument('destAmount', type=float)
		dfcashwithdrawalparserpost.add_argument('bankCd', type=int)
		dfcashwithdrawalparserpost.add_argument('sign', type=str)
		m_args = dfcashwithdrawalparserpost.parse_args(strict=True)
		print('*******************************成功调用********************************************************')
		print(request.headers)
		print(request.url)
		print(m_args)
		print('*******************************成功调用********************************************************')
		if m_args['sign'] is not None:
			return {'code':200,'msg':'成功','paySt':1,'sign':'123xj1i381912311112f332u1123'}
		
'''
下游代付订单查询接口
'''
class QueryTestApi(Resource):
	def post(self):
		m_args = request.json
		print('*******************************成功调用********************************************************')
		print(request.headers)
		print(request.url)
		print(m_args)
		print('*******************************成功调用********************************************************')
		if m_args['sign'] is not None:
			mdata = {}
			mdata['code'] = "123123123"
			mdata['msg'] = '测试'
			mdata['mchntPayforSsn'] = m_args['mchntPayforSsn']
# 			mdata['mchntPayforSsn'] = 1569079438800140571
			mdata['txnId'] = str(int(time.time()))
			mdata['txnDt'] = '2019-09-09 15:15:00'
			mdata['destAmount'] = 20000
			mdata['fee'] = 100
# 			mdata['paySt'] = random.randint(0,3)
			mdata['paySt'] = 2
			yuanMa = ''
			skey = "e0287bdb9df6a5b3ab023d9a51f7a32d"
			for k in sorted(mdata, reverse=False):
				if mdata[k] is not None:
					yuanMa += '%s=%s&' % (k, mdata[k])
			yuanMa = yuanMa[:-1]
			yuanMa += skey
			print(yuanMa)
			md = hashlib.md5()
			md.update(yuanMa.encode())
			sign = md.hexdigest()
			mdata['sign'] = sign
			return mdata
		
'''
上游回调接口
'''
class DFNotifyTestApi(Resource):
	def post(self):
		args = request.json
		print(args)
		
	