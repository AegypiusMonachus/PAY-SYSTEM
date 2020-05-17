from flask import Blueprint
main_blueprint = Blueprint('main', __name__)


@main_blueprint.before_request
def before_request():
	pass


@main_blueprint.after_request
def after_request(response):
	return response


from .views import RequestHeader
main_blueprint.add_url_rule('/requestHeader', view_func=RequestHeader.as_view('requestHeader'))

from .views import TestRequest
main_blueprint.add_url_rule('/testRequest', view_func=TestRequest.as_view('testRequest'))
