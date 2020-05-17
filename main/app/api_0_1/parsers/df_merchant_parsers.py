from flask_restful.reqparse import RequestParser

# post
df_merchant_post = RequestParser(trim=True)
df_merchant_post.add_argument('username', type=str)#用户名
df_merchant_post.add_argument('level', type=int)#预设等级
df_merchant_post.add_argument('mobilephone', type=str)#手机号
df_merchant_post.add_argument('email', type=str)#邮箱
df_merchant_post.add_argument('name', type=str)#真实姓名
df_merchant_post.add_argument('remark', type=str)#备注

# get
df_merchant_get = RequestParser(trim=True)
df_merchant_get.add_argument('page', type=int)
df_merchant_get.add_argument('page_size', type=int)

df_merchant_get.add_argument('mer_code', type=str)

df_merchant_get.add_argument('username', type=str)
df_merchant_get.add_argument('begin_time', type=int)
df_merchant_get.add_argument('end_time', type=int)
df_merchant_get.add_argument('state', type=int)
df_merchant_get.add_argument('level', type=int)


# put
df_merchant_put = RequestParser(trim=True)
df_merchant_put.add_argument('mer_code', type=str, required=True)
df_merchant_put.add_argument('state', type=int)
df_merchant_put.add_argument('level', type=int)
df_merchant_put.add_argument('mobilephone', type=str)
df_merchant_put.add_argument('email', type=str)
df_merchant_put.add_argument('name', type=str)
df_merchant_put.add_argument('remark', type=str)

# 商户充值报表username
df_merchant_recharge = RequestParser(trim=True)
df_merchant_recharge.add_argument('page', type=int)
df_merchant_recharge.add_argument('page_size', type=int)

df_merchant_recharge.add_argument('mer_name', type=str)
df_merchant_recharge.add_argument('begin_time', type=int)
df_merchant_recharge.add_argument('end_time', type=int)