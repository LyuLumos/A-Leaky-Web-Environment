import sqlite3
from flask import Flask, render_template, request, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session # Fix
from sqlalchemy import desc
import hashlib
import time


app = Flask(__name__)
app.config['SECRET_KEY'] = 'TH15_15_N0T_F14G!'
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Session(app)

db = SQLAlchemy(app)



class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, primary_key=True, nullable=False)
    passwd = db.Column(db.Integer)
    email = db.Column(db.Text, unique=True, nullable=False)
    auth = db.Column(db.Integer)


class Category(db.Model):
    __tablename__ = "category"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, unique=True, nullable=False)


class Product(db.Model):
    __tablename__ = "product"
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.Text, nullable=False)
    perprice = db.Column(db.Integer, nullable=False)
    store = db.Column(db.Integer, nullable=False)
    sold = db.Column(db.Text)
    piclink = db.Column(db.Text)
    cateid = db.Column(db.Integer, db.ForeignKey('category.id'))


class History(db.Model):
    __tablename__ = "history"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    num = db.Column(db.Text, nullable=False)
    perprice = db.Column(db.Text, nullable=False)
    sumprice = db.Column(db.Text, nullable=False)
    time = db.Column(db.Text, nullable=False)


db.create_all()
product = Product.query.all()
category = Category.query.all()
carts = []

@app.errorhandler(404)
def page_not_found(e):
    return render_template('lost.html'),404
@app.errorhandler(500)
def page_not_found(e):
    return render_template('lost.html'),500

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/index2')
def index2():
    if 'login_ok' in session:
        if(session['login_ok'] == True):
            product = Product.query.all()
            category = Category.query.all()
            return render_template('index2.html', product=product, category=category)
    return redirect(url_for('index'))
    


@app.route('/lost')
def lost():
    if 'login_ok' in session:
        if(session['login_ok'] == True):
            return render_template('lost.html')
    return redirect(url_for('index'))


# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'GET':
#         if 'login_ok' in session:
#             if session['login_ok'] == True:
#                 return redirect(url_for('index'))
#             else:
#                 return render_template('login.html')
#         else:
#             session['login_ok'] = False
#             return redirect(url_for('index'))
#     else:
#         email = request.form['email']
#         passwd = request.form['pass']
#         sifrelenmis = hashlib.sha256(passwd.encode("utf8")).hexdigest()
#         if User.query.filter_by(email=email, passwd=sifrelenmis).first():
#             veri = User.query.filter_by(
#                 email=email, passwd=sifrelenmis).first()
#             session['login_ok'] = True
#             session['isim'] = veri.name
#             session['id'] = veri.id
#             session['auth'] = veri.auth
#             session['sepet'] = carts
#             return redirect(url_for('index'))
#         else:
#             return redirect(url_for('index'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    # 正常登录
    # http://127.0.0.1:5000/login?Email=%271@1.com%27&psw=1
    # sqlite 注入
    # http://127.0.0.1:5000/login?Email=1%20or%201=1%20or%201=1
    with sqlite3.connect('database.db') as conn:
        em = request.args.get('Email')
        pas = request.args.get('psw')
        print("pas="+str(pas))
        pas = hashlib.sha256(str(pas).encode("utf-8")).hexdigest()
        print(em, pas)
        cur = conn.cursor()
        cur.execute("select * from user where email={email} and passwd= '{passwd}'"
                    .format(email=em, passwd=pas))
        ans = cur.fetchall()
        if len(ans):
            session['login_ok'] = True
            session['isim'] = ans[0][1]
            session['id'] = ans[0][0]
            session['auth'] = ans[0][4]
            session['sepet'] = carts
            return redirect(url_for('index2'))
        else:
            return redirect(url_for('index'))


@app.route('/logout')
def logout():
    session['login_ok'] = False
    session.pop('cart', None)
    session.pop('isim', None)
    session.pop('id', None)
    session.pop('auth', None)
    carts.clear()
    session['sepet'] = carts
    return redirect(url_for('index'))


# @app.route('/findback', methods=['GET', 'POST'])
# def findback():
#     if request.method == 'GET':
#         if 'login_ok' in session:
#             if session['login_ok'] == True:
#                 return redirect(url_for('index'))
#             else:
#                 return render_template('findback.html')
#         else:
#             session['login_ok'] = False
#             return render_template('findback.html')
#     else:
#         try:
#             isim = request.form['username']
#             email = request.form['email']
#             passwd = request.form['pass']
#             sifrelenmis = hashlib.sha256(passwd.encode("utf8")).hexdigest()
#             produ = User(name=isim, passwd=sifrelenmis,
#                              email=email, auth='0')
#             db.session.add(produ)
#             db.session.commit()
#             return redirect(url_for('index'))
#         except:
#             return redirect(url_for('findback'))


@app.route('/cart')
def cart():
    if 'login_ok' in session:
        if(session['login_ok'] == True):
            sepetteki = session["sepet"]
            category = Category.query.all()
            return render_template('cart.html', sepetteki=sepetteki, category=category)
        else:
            return render_template('login.html')
    else:
        session['login_ok'] = False
        return redirect(url_for('index'))


@app.route('/addcart/<urunid>')
def addcart(urunid):
    if 'login_ok' in session:
        if(session['login_ok'] == True):
            urungetir = Product.query.filter_by(id=urunid).first()
            durum = False
            carts = session["sepet"]
            for bul in carts:
                if str(bul['id']) == str(urunid):
                    durum = True
            if carts == []:
                num = 1
                hesap = num * 0.99
                perprice = int(urungetir.perprice) + hesap
                sumprice = num * perprice
                addcart = {
                    'id': urungetir.id,
                    'name': urungetir.name,
                    'perprice': perprice,
                    'piclink': urungetir.piclink,
                    'num': num,
                    'sumprice': sumprice
                }
                carts.append(addcart)
            elif durum == True:
                cart = []
                for bul in carts:
                    if str(bul['id']) == str(urunid):
                        num = int(bul["num"])
                        num += 1
                        hesap = num * 0.99
                        perprice = int(bul['perprice'])
                        sumprice = (perprice * num) + hesap
                        bul['num'] = str(num)
                        bul['sumprice'] = str(sumprice)
                        cart.append(bul)
                    else:
                        cart.append(bul)
            else:
                num = 1
                hesap = num * 0.99
                perprice = int(urungetir.perprice) + hesap
                sumprice = num * perprice

                addcart = {
                    'id': urungetir.id,
                    'name': urungetir.name,
                    'perprice': perprice,
                    'piclink': urungetir.piclink,
                    'num': num,
                    'sumprice': sumprice
                }
                carts.append(addcart)
            session["sepet"] = carts
            return redirect(url_for('cart'))
        else:
            return redirect(url_for('index'))
    else:
        session['login_ok'] = False
        return redirect(url_for('index'))


@app.route('/delete/<urunid>')
def delete(urunid):
    if 'login_ok' in session:
        if(session['login_ok'] == True):
            cart = []
            cart = session["sepet"]
            carts.clear()
            for sil in cart:
                if str(sil['id']) != str(urunid):
                    carts.append(sil)
            session["sepet"] = carts
            return render_template('cart.html', sepetteki=session["sepet"])
        else:
            return redirect(url_for('index'))
    else:
        session['login_ok'] = False
        return redirect(url_for('index'))


@app.route('/clearall', methods=['GET'])
def clearall():
    if 'login_ok' in session:
        if(session['login_ok'] == True):
            carts.clear()
            session["sepet"] = carts
            return redirect(url_for('cart'))
        else:
            return redirect(url_for('index'))
    else:
        session['login_ok'] = False
        return redirect(url_for('index'))


@app.route('/product/<urunid>')
def urun(urunid):
    if session['login_ok'] == True:
        urundetay = Product.query.filter_by(id=urunid).first()
        categories = Category.query.filter_by(id=urundetay.cateid).first()
        category = Category.query.all()
        return render_template('product.html', urundetay=urundetay, categories=categories, category=category)
    else:
        return redirect(url_for('index'))


@app.route('/buy')
def buy():
    if 'login_ok' in session:
        if(session['login_ok'] == True):
            kid = session['id']
            carts = session["sepet"]
            for urun in carts:
                product_id = int(urun["id"])
                num = str(urun["num"])
                urunn = Product.query.filter_by(id=product_id).first()
                urunn.sold += int(num)
                urunn.store -= int(num)
                db.session.add(urunn)
                db.session.commit()
                timestamp = str(time.strftime("%x")+"-"+time.strftime("%X"))
                perprice = urun["perprice"]
                sumprice = urun["sumprice"]
                histo = History(user_id=kid, product_id=product_id,
                                num=num, time=timestamp, perprice=perprice, sumprice=sumprice)
                db.session.add(histo)
                db.session.commit()
            carts.clear()
            session["sepet"] = carts
            return redirect(url_for('cart'))
        else:
            return redirect(url_for('index'))
    else:
        session['login_ok'] = False
        return redirect(url_for('index'))


@app.route('/histo')
def histo():
    if 'login_ok' in session:
        if(session['login_ok'] == True):
            user_id = session["id"]
            siparisverilen = History.query.filter_by(user_id=user_id)
            veri = []
            for itemi in siparisverilen:
                uruncagir = Product.query.filter_by(
                    id=itemi.product_id).first()
                siparislerim = {
                    'name': str(uruncagir.name),
                    'perprice': itemi.perprice,
                    'piclink': str(uruncagir.piclink),
                    'num': itemi.num,
                    'sumprice': itemi.sumprice,
                    'time': itemi.time
                }
                veri.append(siparislerim)
            return render_template('history.html', history=veri, category=category)
        else:
            return redirect(url_for('index'))
    else:
        session['login_ok'] = False
        return redirect(url_for('index'))


@app.route('/catege/<cateid>')
def catege(cateid):
    veri = Product.query.filter_by(cateid=cateid).order_by(desc(Product.sold))
    category = Category.query.all()
    return render_template('index2.html', category=category, product=veri)

@app.route('/finalpro')
def finp():
    if 'login_ok' in session:
        if(session['login_ok'] == True):
            return render_template('final.html')
        else:
            return redirect(url_for('index'))
    else:
        session['login_ok'] = False
        return redirect(url_for('index'))
            

@app.route('/finalbuy', methods=['GET', 'POST'])
def fin():
    if 'login_ok' in session:
        if(session['login_ok'] == True):
            if request.method == 'POST' or request.method == 'GET':
                ans = request.args.get('Time') if request.args.get('Time') else "0"
                # print("ans = "+ ans)
                if int(ans) < int('1640966400'): # 2022.1.1 00:00:00
                    return render_template('lost.html')
                else:
                    return render_template('flag.html')
        else:
            return redirect(url_for('index'))
    else:
        session['login_ok'] = False
        return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
