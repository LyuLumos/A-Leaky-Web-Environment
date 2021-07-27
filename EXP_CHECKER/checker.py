# checker 检测各个功能点是否能满足正常用户的需求

import requests
from flask_session_cookie_manager3 import FSCM


url = 'http://127.0.0.1:5000/'
sqlpayload = 'login?Email=1%20or%201=1%20or%201=1'
payload = 'login?Email={email}&psw={passwd}'.format(email="1x@1y.com", passwd="123456")
adminpayload = 'login?Email={email}&psw={passwd}'.format(email="onlyinchecker@1.com", passwd="123456")
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'
}
session = requests.session()
data = session.post(url+sqlpayload,headers=headers)
if str(data.content).find("Letter")+1:
    print("sql注入成功")
else:
    print("sql注入失败")

# -----------------------------------------------------
# 普通用户正常登录
data = session.post(url+payload, headers=headers)
cookie = session.cookies
sess = cookie.get_dict()
text = FSCM.decode(sess['session']).decode("utf-8")
print("Session 解码为："+text)

# get final product
data3 = session.post(url+"finalpro", headers=headers)
if str(data3.content).find("theElderWand") != -1:
    print("普通用户访问隐藏页面成功")
else:
    print("普通用户访问隐藏页面失败")


data3 = session.post(url+'finalbuy', headers=headers)
if data3.status_code >= 400 or str(data3.content).find('ERROR')+1:
    print("普通用户购买失败")
else:
    print("普通用户购买成功")


# -----------------------------------------------------
# 特权用户正常登录
data = session.post(url+adminpayload, headers=headers)
print(url+adminpayload)
cookie = session.cookies
sess = cookie.get_dict()
text = FSCM.decode(sess['session']).decode("utf-8")
print("Session 解码为："+text)

# get final product
data3 = session.post(url+"finalpro", headers=headers)
if str(data3.content).find("theElderWand") != -1:
    print("特权用户访问隐藏页面成功")
else:
    print("特权用户访问隐藏页面失败")


data3 = session.post(url+'finalbuy', headers=headers)
# print(data3.content)
if data3.status_code >= 400 or str(data3.content).find('ERROR')+1:
    print("特权用户购买失败")
else:
    print("特权用户购买成功")