import unittest
import requests


class TestMethods(unittest.TestCase):
	def setUp(self):
		pass

	def tearDown(self):
		pass

	def test_bank_trade(self):
		payload = {
			"amount": 5,
			"order_no": "1234111120002",
			"pay_time": 1568532189
		}

		response = requests.post('http://manage.devqp.info/pay/0.1/banknotify/44', json=payload)
		print(response.text)


if __name__ == '__main__':
	suite = unittest.TestSuite()
	suite.addTest(TestMethods('test_bank_trade'))

	runner = unittest.TextTestRunner()
	runner.run(suite)