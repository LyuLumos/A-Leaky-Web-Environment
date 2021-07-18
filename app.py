from flask import Flask, render_template, request, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
import hashlib
import time
app = Flask(__name__)
app.secret_key = 'samet'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
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


@app.route('/')
def index():
    product = Product.query.all()
    category = Category.query.all()
    # print(product, category)
    return render_template('index.html', product=product, category=category)

# 丢失界面
@app.route('/lost')
def lost():
    return render_template('lost.html')

# 登录
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if 'login_ok' in session:
            if session['login_ok'] == True:
                return redirect(url_for('index'))
            else:
                return render_template('login.html')
        else:
            session['login_ok'] = False
            return redirect(url_for('login'))
    else:
        email = request.form['email']
        passwd = request.form['pass']
        sifrelenmis = hashlib.sha256(passwd.encode("utf8")).hexdigest()

        print(sifrelenmis)
        if User.query.filter_by(email=email, passwd=sifrelenmis).first():
            veri = User.query.filter_by(
                email=email, passwd=sifrelenmis).first()
            session['login_ok'] = True
            session['isim'] = veri.name
            session['id'] = veri.id
            session['auth'] = veri.auth
            session['sepet'] = carts
            return redirect(url_for('index'))
        else:
            return redirect(url_for('login'))


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


@app.route('/findback', methods=['GET', 'POST'])
def findback():
    if request.method == 'GET':
        if 'login_ok' in session:
            if session['login_ok'] == True:
                return redirect(url_for('index'))
            else:
                return render_template('findback.html')
        else:
            session['login_ok'] = False
            return render_template('findback.html')
    else:
        try:
            isim = request.form['username']
            email = request.form['email']
            passwd = request.form['pass']
            sifrelenmis = hashlib.sha256(passwd.encode("utf8")).hexdigest()
            kullanıcı = User(name=isim, passwd=sifrelenmis,
                             email=email, auth='0')
            db.session.add(kullanıcı)
            db.session.commit()
            return redirect(url_for('index'))
        except:
            return redirect(url_for('findback'))



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
        return redirect(url_for('login'))


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
            return redirect(url_for('login'))
    else:
        session['login_ok'] = False
        return redirect(url_for('login'))


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
            return redirect(url_for('login'))
    else:
        session['login_ok'] = False
        return redirect(url_for('login'))


@app.route('/clearall', methods=['GET'])
def clearall():
    if 'login_ok' in session:
        if(session['login_ok'] == True):
            carts.clear()
            session["sepet"] = carts
            return redirect(url_for('cart'))
        else:
            return redirect(url_for('login'))
    else:
        session['login_ok'] = False
        return redirect(url_for('login'))


@app.route('/product/<urunid>')
def urun(urunid):
    if session['login_ok'] == True:
        urundetay = Product.query.filter_by(id=urunid).first()
        categories = Category.query.filter_by(id=urundetay.cateid).first()
        category = Category.query.all()
        return render_template('product.html', urundetay=urundetay, categories=categories, category=category)
    else:
        return redirect(url_for('login'))


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
            return redirect(url_for('login'))
    else:
        session['login_ok'] = False
        return redirect(url_for('login'))


@app.route('/histo')
def histo():
    if 'login_ok' in session:
        if(session['login_ok'] == True):
            user_id = session["id"]
            siparisverilen = History.query.filter_by(user_id=user_id)
            veri = []
            for itemi in siparisverilen:
                uruncagir = Product.query.filter_by(id=itemi.product_id).first()
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
            return redirect(url_for('login'))
    else:
        session['login_ok'] = False
        return redirect(url_for('login'))


@app.route('/catege/<cateid>')
def catege(cateid):
    veri = Product.query.filter_by(cateid=cateid).order_by(desc(Product.sold))
    category = Category.query.all()
    return render_template('index.html', category=category, product=veri)


if __name__ == '__main__':
    app.run(debug=True)
