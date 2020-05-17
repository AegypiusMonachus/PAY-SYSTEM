import unittest
import requests
import time, json
import hashlib


class TestCase(unittest.TestCase):
	def setUp(self):
		pass

	def tearDown(self):
		pass

	def test_online_trade(self):
		mer_code = '8576a8e7f57842428f5f8141f7afa829'
		amount = 10
		user_name = '测试1'
		notify_url = 'http://500wm.devqp.info/pay/0.1/test'
		org_order_time = str(int(time.time()))
		pay_type = 1008
		remark = ''
		payload = {'user_name': user_name,
				   'mer_code': mer_code,
				   'amount': amount,
				   'notify_url': notify_url,
				   'org_order_time': org_order_time,
				   'pay_type': pay_type,
				   'remark': remark,
				   'org_order_no': 105,
				   }
		yuanMa = 'amount=' + str(
			amount) + '&mer_code=' + mer_code + '&notify_url=' + notify_url + '&org_order_no=' + str(105) + \
				 '&org_order_time=' + org_order_time + '&pay_type=' + str(
			pay_type) + '&user_name=' + user_name + '118fb24eb04874d3e71b9b8db592320a'

		md = hashlib.md5()
		md.update(yuanMa.encode())
		sign = md.hexdigest()
		payload['sign'] = sign
		headers = {'content-type': 'application/json'}
		url = 'http://manage.devqp.info/pay/0.1/gateway'

		response = requests.post(url, data=json.dumps(payload), headers=headers)
		print(response.text)


if __name__ == '__main__':
	suite = unittest.TestSuite()
	suite.addTest(TestCase('test_online_trade'))

	runner = unittest.TextTestRunner()
	runner.run(suite)
