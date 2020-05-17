from flask_restful.reqparse import RequestParser
from ..utils import *

MerChantparser = RequestParser(trim=True)
MerChantparser.add_argument('page', type=int)
MerChantparser.add_argument('page_size', type=int)

MerChantparser.add_argument('mer_code', type=str)
MerChantparser.add_argument('username', type=str)
MerChantparser.add_argument('begin_time', type=int)
MerChantparser.add_argument('end_time', type=int)
MerChantparser.add_argument('begin_wrdraw_amount', type=int)
MerChantparser.add_argument('end_wrdraw_amount', type=int)
MerChantparser.add_argument('parent_code', type=str)
MerChantparser.add_argument('parent_name', type=str)
MerChantparser.add_argument('state', type=int)
MerChantparser.add_argument('level', type=int)


MerChantparserPost = RequestParser(trim=True)

MerChantparserPost.add_argument('page', type=int,default = DEFAULT_PAGE)
MerChantparserPost.add_argument('page_size', type=int,default = DEFAULT_PAGE_SIZE)

MerChantparserPost.add_argument('username', type=str)
MerChantparserPost.add_argument('type', type=int)

MerChantparserPost.add_argument('parent_code', type=str)
MerChantparserPost.add_argument('parent_name', type=str)
MerChantparserPost.add_argument('rate')
MerChantparserPost.add_argument('level', type=int)
MerChantparserPost.add_argument('wrdraw_amount', type=float)
MerChantparserPost.add_argument('mobilephone', type=str)
MerChantparserPost.add_argument('email', type=str)
MerChantparserPost.add_argument('name', type=str)
MerChantparserPost.add_argument('remark', type=str)


MerChantparserPut = RequestParser(trim=True)
MerChantparserPut.add_argument('parent_code', type=int)
MerChantparserPut.add_argument('rate')
MerChantparserPut.add_argument('code', type=str)
MerChantparserPut.add_argument('state', type=int)

MerChantparserPut.add_argument('level', type=int)
MerChantparserPut.add_argument('mobilephone', type=str)
MerChantparserPut.add_argument('email', type=str)
MerChantparserPut.add_argument('name', type=str)
MerChantparserPut.add_argument('wrdraw_amount', type=float)
MerChantparserPut.add_argument('remark', type=str)