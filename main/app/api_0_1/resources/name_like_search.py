from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from app.api_0_1.common import make_response
from ...models.merchant_dao import MerchantDao
from app.models import db




class NameLikeSearch(Resource):
	def get(self):
		parser = RequestParser(trim=True)
		parser.add_argument('username', type=str)
		parser.add_argument('type', type=int)
		args = parser.parse_args(strict=True)

		res_name = None
		if args['type'] == 1 or args['type'] == 2:
			res_name = db.session.query(MerchantDao).filter(MerchantDao.username.like(args['username'] + "%")).order_by(MerchantDao.id.desc()).limit(10).all()

		# 平台商户看板
		if args['type'] == 3:
			res_name = db.session.query(MerchantDao).filter(MerchantDao.username.like(args['username'] + "%"), MerchantDao.type == 1).order_by(MerchantDao.id.desc()).limit(10).all()

		# 平台代理看板
		if args['type'] == 4:
			res_name = db.session.query(MerchantDao).filter(MerchantDao.username.like(args['username'] + "%"), MerchantDao.type == 2).order_by(MerchantDao.id.desc()).limit(10).all()

		result = []
		for i in res_name:
			result.append({
				"username": i.username
			})
		return make_response(result)


