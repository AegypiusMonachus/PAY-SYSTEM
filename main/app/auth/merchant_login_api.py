from flask import redirect,request
from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from config import  Config
class MerchantLoginAPI(Resource):
    def post(self):
        parser = RequestParser(trim=True)
        parser.add_argument('username', type=str)
        parser.add_argument('password', type=str)
        args = parser.parse_args(strict=True)
        uri = Config.OAUTH2_SERVICE_URI + '/oauth2/merchant?username=%s&password=%s&redirect_uri=%s&client_id=%s' %(args['username'], args['password'],Config.MERCHANT_URI, args['username'])
        return redirect(uri)
#         token = mjson['access_token']
#         redisImpl = AuthRedisManager.get_redisImpl()
#         redisImpl.set(token, mjson)
#         redisImpl.expire(token, 3600 * 24 * 7)

class MerchantPassportAPI(Resource):
    def get(self):
#         parser = RequestParser(trim=True)
#         parser.add_argument('code', type=str)
#         parser.add_argument('client_id', type=str)
#         parser.add_argument('grant_type', type=int)
#         args = parser.parse_args(strict=True)      
        args = request.args
        uri = Config.OAUTH2_SERVICE_URI + '/oauth2/merchant?grant_type=%s&code=%s&redirect_uri=%s&client_id=%s' % (args['grant_type'],args['code'], Config.MERCHANT_URI, args['client_id'])
        return redirect(uri)
