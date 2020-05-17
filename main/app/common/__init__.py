import random
from app.models import db
import time
import os,string
from pyzbar import pyzbar
from PIL import Image
import qrcode
from config import Config
from decimal import *
from app.models.transaction_code_dao import Qrcode
from sqlalchemy import func
# 时间戳+支付类型+四位随机数+商户id  --> 生成订单号

def creat_order_no(pay_type,merchant_id):
    shijianchuo = str(int(time.time()))
    suijifour = str(random.randint(1000, 9999))
    order_no = str(shijianchuo + str(pay_type) + suijifour + str(merchant_id))
    return order_no

# 解析二维码，生成带logo的二维码
class CreatNewQrcode():
    def __init__(self, name):
        self.__context = name
        self.qrcodeData = None

    def creat_new_qrcode(self):
        path = os.path.abspath(Config.STATIC_FOLDER )
        file_path = path + "/" + self.__context
        if os.path.isfile(file_path):
            img = Image.open(file_path)
            txt_list = pyzbar.decode(img)
            for txt in txt_list:
                codeData = txt.data.decode("utf-8")
                self.qrcodeData = codeData
        else:
            self.error_code = 9017
            self.error_msg = '图片错误'
            self.success = False
            return
        new_code_name = self.creat_new_logo_qrcode()
        return new_code_name

    # 生成附加logo的二维码
    def creat_new_logo_qrcode(self):
        data = self.qrcodeData
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=20,
            border=2,
        )
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill_color="#000", back_color="white")
        path1 = os.path.abspath(Config.STATIC_FOLDER )
        path2 = path1 + "/9618.png"
        if not os.path.isfile(path2):
            self.error_code = 9017
            self.error_msg = 'logo图片错误'
            self.success = False
            return
        icon = Image.open(path2)
        img_w, img_h = img.size
        factor = 3
        size_w = int(img_w / factor)
        size_h = int(img_h / factor)
        icon_w, icon_h = icon.size
        if icon_w < size_w:
            icon_w = size_w
        if icon_h < size_h:
            icon_h = size_h
        icon = icon.resize((icon_w, icon_h), Image.ANTIALIAS)
        w = int((img_w - icon_w) / 2)
        h = int((img_h - icon_h) / 2)
        img.paste(icon, (w, h), mask=None)
        file_name = ''.join(random.sample(string.ascii_letters + string.digits, 16)) + '.png'
        path = path1 + '/' + file_name
        print(path)
        with open(path, 'wb') as f:
            img.save(f)
        return file_name

# 保留两位小数，四舍五入
def keep_two(v):
    c = v.quantize(Decimal('0.00'))
    return c

# 保留两位小数，多余舍去
def keep_two_del(v):
    c = v.quantize(Decimal('0.00'), rounding=ROUND_DOWN)
    return c

# 保留三位小数，四舍五入
def keep_three(v):
    c = v.quantize(Decimal('0.000'))
    return c

# 保留三位小数，多余舍去
def keep_three_del(v):
    c = v.quantize(Decimal('0.000'), rounding=ROUND_DOWN)
    return c

# 开启/关闭二维码
def BEQRcode(qrcodes,state):
    for qrcode in qrcodes:
        qrcode.state = state
        try:
            db.session.add(qrcode)
            db.session.commit()
        except:
            db.session.rollback()
            db.session.remove()
            return False
    return True


# 二维码编号
def QRcodeNum(bank_id, receive_id):
    bank_id = str(bank_id)
    bank_id = bank_id.zfill(2)
    code_no = bank_id + str(receive_id)
    code_count = db.session.query(Qrcode).filter(Qrcode.code.like(code_no + '%')).count()
    end_three = str(code_count+1)
    end_three = end_three.zfill(3)
    code_num = code_no + end_three
    return  code_num

def formatDecimal(value):
    if isinstance(value, float):
        value = Decimal.from_float(value)
    if isinstance(value, int) or isinstance(value, str):
        value = Decimal(value)
    if not isinstance(value, Decimal):
        raise ValueError
    value = value.quantize(Decimal('1.000'))
    return value

def formatDecimal_two(value):
    if isinstance(value, float):
        value = Decimal.from_float(value)
    if isinstance(value, int) or isinstance(value, str):
        value = Decimal(value)
    if not isinstance(value, Decimal):
        raise ValueError
    value = value.quantize(Decimal('1.00'))
    return value

def date_to_int(m_date):
    return int(time.mktime(time.strptime(m_date, '%Y-%m-%d %H:%M:%S')))