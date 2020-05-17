# MD5加密

from hashlib import md5
import time,random

import uuid

def encrypt_md5(args):
    # 创建md5对象
    new_md5 = md5()
    new_md5.update(args.encode(encoding='utf-8'))
    # 加密
    return new_md5.hexdigest()

#生成随机商户号

def merRange():
    uid = str(uuid.uuid4())
    suid = ''.join(uid.split('-'))

    return suid

# 生成随机的盐
def rando():
    salf = str(random.randint(10000, 999999))
    return salf

# # 生成随机加密文
# def merRange(args):
#     code = str(random.randint(10000,999999))
#     return code


# 生成随机的订单号
def makeOrder(id):
    order_id = str(id) + str(int(time.time())) + str(random.randint(1000,9999))
    return order_id
