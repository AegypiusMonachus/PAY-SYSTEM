from flask_restful.reqparse import RequestParser

# post
df_agent_post = RequestParser(trim=True)
df_agent_post.add_argument('username', type=str) #用户名
df_agent_post.add_argument('rateInputs', type=str) #费率设定
df_agent_post.add_argument('level', type=str) #等级
df_agent_post.add_argument('mobilephone', type=str) #手机
df_agent_post.add_argument('email', type=str)
df_agent_post.add_argument('name', type=str)
df_agent_post.add_argument('remark', type=str)


# get
df_agent_get = RequestParser(trim=True)
df_agent_get.add_argument('page', type=int)
df_agent_get.add_argument('page_size', type=int)
df_agent_get.add_argument('agent_code', type=str)
df_agent_get.add_argument('username', type=str)
df_agent_get.add_argument('begin_time', type=int)
df_agent_get.add_argument('end_time', type=int)
df_agent_get.add_argument('state', type=int)
df_agent_get.add_argument('level', type=int)


# put
df_agent_put = RequestParser(trim=True)
df_agent_put.add_argument('rateInputs', type=str) #费率设定
df_agent_put.add_argument('level', type=int) #等级
df_agent_put.add_argument('state', type=int) #状态
df_agent_put.add_argument('mobilephone', type=str) #手机
df_agent_put.add_argument('email', type=str)
df_agent_put.add_argument('name', type=str)
df_agent_put.add_argument('remark', type=str)
df_agent_put.add_argument('agent_code', type=str)
df_agent_put.add_argument('agent_name', type=str)