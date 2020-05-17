def create_app(config_name):
	from flask import Flask
	app = Flask(__name__)

	from flask_cors import CORS
	CORS(app)

	from config import config_mapping
	app.config.from_object(config_mapping[config_name])
	config_mapping[config_name].init_app(app)

	from itsdangerous import JSONWebSignatureSerializer
	app.serializer = JSONWebSignatureSerializer('1E7AB4FFF67A59726E6681C2E87F68F0')

	from .models import db
	db.init_app(app)

	from app.redis.redisConnectionManager import (AuthRedisManager,PayRedisManager)
	AuthRedisManager.init_app(app, 3)
	PayRedisManager.init_app(app, 2)
# 	from app.schedule import scheduler
# 	scheduler.init_app(app)
# 	scheduler.start()

	from .auth import (auth_blueprint,df_auth_blueprint)
	app.register_blueprint(auth_blueprint, url_prefix='/payment/auth')
	app.register_blueprint(df_auth_blueprint, url_prefix='/df/payment/auth')
	
	from .oauth2 import (oauth2_blueprint,df_oauth2_blueprint)
	app.register_blueprint(oauth2_blueprint, url_prefix='/oauth2')
	app.register_blueprint(df_oauth2_blueprint, url_prefix='/df/oauth2')
	
	from .main import main_blueprint
	app.register_blueprint(main_blueprint, url_prefix='/payment/main')

	from .api_0_1 import (api_0_1_blueprint,df_api_0_1_blueprint)
	app.register_blueprint(api_0_1_blueprint, url_prefix='/payment/0.1')
	app.register_blueprint(df_api_0_1_blueprint, url_prefix='/df/payment/0.1')

	from .payment import payment_blueprint
	app.register_blueprint(payment_blueprint, url_prefix='/pay/0.1')

	from .member import member_blueprint,df_member_blueprint
	app.register_blueprint(member_blueprint, url_prefix='/merchant/0.1')
	app.register_blueprint(df_member_blueprint, url_prefix='/df/merchant/0.1')

	from .agentspay import agentpay_blueprint
	app.register_blueprint(agentpay_blueprint, url_prefix='/df/agentpay/0.1')
	
	from .api_0_1_df import api_0_1_df_blueprint
	app.register_blueprint(api_0_1_df_blueprint, url_prefix='/df/payment/0.1')
	

	@app.before_first_request
	def before_first_request():
		from .extensions import code_manager
		code_manager.refresh()

	@app.before_request
	def before_request():
		pass

	@app.after_request
	def after_request(response):
		return response

	@app.errorhandler(SyntaxError)
	def syntax_error_handler(error):
		app.logger.exception(error)

	@app.route('/payment/static/<filename>', methods=['GET'])
	def get_static_file(filename):
		from flask import request
		from flask.json import jsonify
		from app.auth.common import verify_token

		token = request.args
		token = token['token']
		print(token)
		if not token:
			return jsonify({
				'success': False,
				'errorCode': 400,
			})
		if not verify_token(token):
			return jsonify({
				'success': False,
				'errorCode': 401
			})
		return app.send_static_file(filename)

	return app
