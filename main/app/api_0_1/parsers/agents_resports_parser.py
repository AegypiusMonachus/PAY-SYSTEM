from flask_restful.reqparse import RequestParser
from ..utils import *



agentsparserresports = RequestParser(trim=True)
agentsparserresports.add_argument('page', type=int)
agentsparserresports.add_argument('page_size', type=int)

agentsparserresports.add_argument('begin_time', type=int)
agentsparserresports.add_argument('end_time', type=int)
agentsparserresports.add_argument('state', type=int)



agentsparserresportsguanli = RequestParser(trim=True)
agentsparserresportsguanli.add_argument('page', type=int)
agentsparserresportsguanli.add_argument('page_size', type=int)

agentsparserresportsguanli.add_argument('mer_username', type=str)
agentsparserresportsguanli.add_argument('begin_time', type=int)
agentsparserresportsguanli.add_argument('end_time', type=int)
agentsparserresportsguanli.add_argument('state', type=int)

# agentsparserresportstotal = RequestParser(trim=True)
#
# agentsparserresportstotal.add_argument('begin_time', type=int)
# agentsparserresportstotal.add_argument('end_time', type=int)
# agentsparserresportstotal.add_argument('state', type=int)


agentsparserresportstotalguanli = RequestParser(trim=True)

agentsparserresportstotalguanli.add_argument('page', type=int)
agentsparserresportstotalguanli.add_argument('page_size', type=int)
agentsparserresportstotalguanli.add_argument('mer_username', type=str)
agentsparserresportstotalguanli.add_argument('begin_time', type=int)
agentsparserresportstotalguanli.add_argument('end_time', type=int)
agentsparserresportstotalguanli.add_argument('state', type=int)