from flask import Flask, render_template, request, redirect, url_for
import pymysql
import traceback

app = Flask(__name__)

# MySQL
# create database if not exists Test_db;
# use Test_db;
# create table if not exists user 
# (
# user varchar(40),
# password varchar(40)
# );

# insert into 
#user (user, password) values('admin', 'fd063329ee736949b644e77b5919d1a2');
# select * from user;

# md5(english.encode('utf8')).hexdigest()

# create user alice identified by '528113';
# grant select, insert on Test_db.user to 'alice';

@app.route('/')
def login():
    return render_template('login.html')


@app.route('/regist')
def regist():
    return render_template('regist.html')


@app.route('/registuser')
def getRegistRequest():
    db = pymysql.connect(host="localhost", user="root", passwd="123456", database="Test_db")
    cursor = db.cursor()
    sql = "INSERT INTO user(user, password) VALUES ('{user}', '{passwd}')" \
        .format(user=str(request.args.get('user')),
                passwd=str(request.args.get('password')))
    try:
        cursor.execute(sql)
        db.commit()
        return redirect(url_for('login'))
    except:
        traceback.print_exc()
        db.rollback()
        return '注册失败'
    db.close()


# http://127.0.0.1:5000/login?user=1%27%20or%20%271%27=%271&password=1%27%20or%20%271%27=%271
@app.route('/login')
def getLoginRequest():
    db = pymysql.connect(host="localhost", user="root", passwd="123456", database="Test_db")
    cursor = db.cursor()
    sql = "select * from user where user='{user}' and password= '{passwd}'" \
        .format(user=str(request.args.get('user')),
                passwd=str(request.args.get('password')))
    print("sql=" + sql)
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        print("login success: " + str(len(results)))
        if len(results) == 1:
            return '登录成功'
        else:
            return '用户名或密码不正确'
        db.commit()
    except:
        traceback.print_exc()
        db.rollback()
    db.close()


import time
@app.route('/finalbuy',  methods=['GET', 'POST'])
def buyFinalProduct():
    if request.method == 'POST':
        ans = str(request.args.get(['time']))
        if int(ans) < int('3408192000'): # 2078.1.1 00:00:00
            print("FAILED")
        else:
            return render_template('flag.html')



if __name__ == '__main__':
    app.run(debug=True)
