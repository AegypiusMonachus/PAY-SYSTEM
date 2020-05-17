from flask import Blueprint
payment_blueprint = Blueprint('payment', __name__)


@payment_blueprint.before_request
def before_request():
    pass


@payment_blueprint.after_request
def after_request(response):
    return response


from flask_restful import Api
api = Api(payment_blueprint)

from .gateway_api import GatewayAPI
api.add_resource(GatewayAPI, '/gateway')

from .bank_notify_api import BankNodifyAPI
api.add_resource(BankNodifyAPI, '/banknotify/<string:qrcode>')

from .gateway_api import TempCodeAPI
api.add_resource(TempCodeAPI, '/tempcode/<string:tempcode>')

from .gateway_api import VerifyTempCodeAPI
api.add_resource(VerifyTempCodeAPI, '/verify/<string:tempcode>')

from app.payment.test_api import TestApi
api.add_resource(TestApi, '/test')

from .gateway_api import CancelOrderApi, Reconfirmed, ReconfirmedSuccessed
api.add_resource(CancelOrderApi, '/cancel')
api.add_resource(Reconfirmed, '/reconfirmed')
api.add_resource(ReconfirmedSuccessed, '/reconfirmed/successed')


from .df_amount_api import DfAmount
api.add_resource(DfAmount, '/dfamount')


from .test_amount_api import TestAmount
api.add_resource(TestAmount, '/test/amount')