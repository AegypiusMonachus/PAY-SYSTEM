from flask import Blueprint
api_blueprint = Blueprint('api', __name__)


@api_blueprint.before_request
def before_request():
    pass


@api_blueprint.after_request
def after_request(response):
    return response


from flask_restful import Api
api = Api(api_blueprint)


from .resources import Orders
api.add_resource(Orders, '/orders')
