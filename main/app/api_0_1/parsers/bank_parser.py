from flask_restful.reqparse import RequestParser

bankParsers = RequestParser(trim=True)

bankParsers.add_argument('username', type=str)
bankParsers.add_argument('bank_id', type=int)


bankParserspost = RequestParser(trim=True)
bankParserspost.add_argument('username', type=str)
bankParserspost.add_argument('bankNumber', type=int)
bankParserspost.add_argument('numbers', type=str)
bankParserspost.add_argument('bankname', type=str)
