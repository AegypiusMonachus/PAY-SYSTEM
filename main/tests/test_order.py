import unittest
import requests


class TestCase(unittest.TestCase):
	def setUp(self):
		pass

	def tearDown(self):
		pass

	def test_can_cancel_order(self):
		response = requests.post('http://manage.devqp.info/pay/0.1/cancel', json={'order_no': '156860603710021853111'})
		print(response.text)


if __name__ == '__main__':
	suite = unittest.TestSuite()
	suite.addTest(TestCase('test_can_cancel_order'))

	runner = unittest.TextTestRunner()
	runner.run(suite)
