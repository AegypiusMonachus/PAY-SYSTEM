def create_app(config_name):
	from flask import Flask
	app = Flask(__name__)

	from flask_cors import CORS
	CORS(app)

	from config import config_mapping
	app.config.from_object(config_mapping[config_name])
	config_mapping[config_name].init_app(app)

	from .models import db
	db.init_app(app)

	from .extensions import order_manager
	order_manager.init_app(app)

	from .api import api_blueprint
	app.register_blueprint(api_blueprint, url_prefix='/api/0.1')
	
	@app.before_first_request
	def before_first_request():
		pass

	@app.before_request
	def before_request():
		pass

	@app.after_request
	def after_request(response):
		return response

	@app.errorhandler(SyntaxError)
	def syntax_error_handler(error):
		app.logger.exception(error)

	app.logger.info('APP START')
	return app
