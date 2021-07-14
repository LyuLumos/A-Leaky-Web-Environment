from flask import Flask, render_template, request, redirect, url_for
import pymysql
import traceback

app = Flask(__name__)

# app.secret_key='123456'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:mysql@127.0.0.1/users'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)

# MySQL
# create database if not exists Test_db;
# use Test_db;
# create table if not exists user 
# (
# user varchar(30),
# password varchar(30)
# );

# insert into user (user, password) values('admin', '123478');
# select * from user;


@app.route('/')
def login():
    return render_template('login.html')
 

@app.route('/regist')
def regist():
    return render_template('regist.html')


@app.route('/registuser')
def getRegistRequest():
    db = pymysql.connect(host="localhost",user="root",passwd="123456",database="Test_db" )
    cursor = db.cursor()
    sql = "INSERT INTO user(user, password) VALUES ('{user}', '{passwd}')".format(user=str(request.args.get('user')), passwd=str(request.args.get('password')))
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
    db = pymysql.connect(host="localhost",user="root",passwd="123456",database="Test_db" )
    cursor = db.cursor()
    sql = "select * from user where user='{user}' and password= '{passwd}'".format(user=str(request.args.get('user')), passwd=str(request.args.get('password')))
    print("sql="+sql)
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        print("login success" + len(results))
        if len(results)==1:
            return '登录成功'
        else:
            return '用户名或密码不正确'
        db.commit()
    except:
        traceback.print_exc()
        db.rollback()
    db.close()
    
 
if __name__ == '__main__':
    app.run(debug=True)
