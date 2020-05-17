from flask_restful.reqparse import RequestParser

# post
from app.api_0_1.utils import DEFAULT_PAGE, DEFAULT_PAGE_SIZE

qrcodeparserpost = RequestParser(trim=True)
qrcodeparserpost.add_argument('name', type=str)
qrcodeparserpost.add_argument('qr_image', type=str)
qrcodeparserpost.add_argument('bank_id', type=int)
qrcodeparserpost.add_argument('bank_num', type=int)
qrcodeparserpost.add_argument('rate')
qrcodeparserpost.add_argument('receive_member', type=str)
qrcodeparserpost.add_argument('remark', type=str)
qrcodeparserpost.add_argument('bank_account', type=str)
qrcodeparserpost.add_argument('valid_time', type=int)
qrcodeparserpost.add_argument('levels')
qrcodeparserpost.add_argument('phone_number', type=str)
qrcodeparserpost.add_argument('lower_amount', type=float)
qrcodeparserpost.add_argument('upper_amount', type=float)
qrcodeparserpost.add_argument('ori_type', type=int)
qrcodeparserpost.add_argument('new_qrcode', type=str)
qrcodeparserpost.add_argument('labels', type=str)


#get
qrcodeparserget = RequestParser(trim=True)
qrcodeparserget.add_argument('page', type=int, default=DEFAULT_PAGE)
qrcodeparserget.add_argument('page_size', type=int, default=DEFAULT_PAGE_SIZE)
qrcodeparserget.add_argument('state', type=int)
qrcodeparserget.add_argument('code', type=str)
qrcodeparserget.add_argument('bank_account', type=int)
qrcodeparserget.add_argument('name', type=str)
qrcodeparserget.add_argument('selectPayType', type=str)


# put
qrcodeparserput = RequestParser(trim=True)
qrcodeparserput.add_argument('state', type=int)
qrcodeparserput.add_argument('code', type=str)
qrcodeparserput.add_argument('qr_image', type=str)
qrcodeparserput.add_argument('new_qrcode', type=str)
qrcodeparserput.add_argument('valid_time', type=int)
qrcodeparserput.add_argument('name', type=str)
qrcodeparserput.add_argument('levels')
qrcodeparserput.add_argument('receive_member',type=str)
