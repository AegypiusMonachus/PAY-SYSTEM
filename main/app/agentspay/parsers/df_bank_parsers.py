from flask_restful.reqparse import RequestParser


dfbankparser = RequestParser(trim=True)

dfbankparser.add_argument('bankId', type=str)


dfbankpostparser = RequestParser(trim=True)

dfbankpostparser.add_argument('bankId', type=int)
dfbankpostparser.add_argument('name', type=str)
dfbankpostparser.add_argument('bankNumber', type=str)
dfbankpostparser.add_argument('d_bank', type=int)