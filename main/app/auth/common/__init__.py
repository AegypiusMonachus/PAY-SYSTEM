from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth, MultiAuth
basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth()
multi_auth = MultiAuth(basic_auth, token_auth)
from flask import g
from app.redis.redisConnectionManager import AuthRedisManager
import json
class Object:
	pass

@token_auth.verify_token
def verify_token(token=None):
	from flask import current_app
	if not token:
		return False
	redisImpl = AuthRedisManager.get_redisImpl()
	merjson = redisImpl.get(token)
	g.current_user = None
	if merjson:
		mer = json.loads(merjson)
		g.current_member = Object()
		g.current_member.username = mer['client_id']
		g.current_member.type = mer['grant_type']
		g.current_member.scope = mer['scope']
		return True
	else:
		return False
