from flask import Flask
from flask import render_template
from flask import request  

app = Flask(__name__)

    
# 登录
@app.route('/')
def login():
    return render_template('login.html')
 
# 注册
@app.route('/regist')
def regist():
    return render_template('regist.html')
    

