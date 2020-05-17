from flask_restful.reqparse import RequestParser
from ..utils import *



agentsparser = RequestParser(trim=True)
agentsparser.add_argument('page', type=int)
agentsparser.add_argument('page_size', type=int)

agentsparser.add_argument('mer_code', type=str)
agentsparser.add_argument('username', type=str)
agentsparser.add_argument('begin_time', type=int)
agentsparser.add_argument('end_time', type=int)
agentsparser.add_argument('state', type=int)


agentsparserpost = RequestParser(trim=True)
agentsparserpost.add_argument('username', type=str)
agentsparserpost.add_argument('rate', type=str)
agentsparserpost.add_argument('wrdraw_amount', type=float)
agentsparserpost.add_argument('state', type=int)
agentsparserpost.add_argument('level', type=str)
agentsparserpost.add_argument('mobilephone', type=str)
agentsparserpost.add_argument('email', type=str)
agentsparserpost.add_argument('name', type=str)
agentsparserpost.add_argument('remark', type=str)


agentsparserput = RequestParser(trim=True)
agentsparserput.add_argument('rate', type=str)
agentsparserput.add_argument('level', type=int)
agentsparserput.add_argument('state', type=int)
agentsparserput.add_argument('mobilephone', type=str)
agentsparserput.add_argument('email', type=str)
agentsparserput.add_argument('name', type=str)
agentsparserput.add_argument('remark', type=str)
agentsparserput.add_argument('wrdraw_amount', type=float)