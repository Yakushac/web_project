from flask import Flask, render_template, make_response, request, redirect
from data import db_session
from data.db_session import create_session
from data.users import User
from data.products import Products
from data.liked_products import Liked
import datetime
from data.login_form import LoginForm, RegisterForm, AddProduct
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'sell_web_site'


def main():
    db_session.global_init("db/sells.db")
    app.run()


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route("/cookie_test")
def cookie_test():
    visits_count = int(request.cookies.get("visits_count", 0))
    if visits_count:
        res = make_response(
            f"Вы пришли на эту страницу {visits_count + 1} раз")
        res.set_cookie("visits_count", str(visits_count + 1),
                       max_age=60 * 60 * 24 * 365 * 2)
    else:
        res = make_response(
            "Вы пришли на эту страницу в первый раз за последние 2 года")
        res.set_cookie("visits_count", '1',
                       max_age=60 * 60 * 24 * 365 * 2)
    return res


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/home')
def home():
    db_sess = db_session.create_session()
    products = db_sess.query(Products).filter(Products.user_id == current_user.id)
    if current_user.is_authenticated:
        return render_template('home.html', name=current_user.name, email=current_user.email,
                               about=current_user.about, products=products)
    else:
        return redirect('/')


@app.route("/")
def main_page():
    db_sess = db_session.create_session()
    products = db_sess.query(Products).filter(Products.is_private != True)
    return render_template("main_page.html", all_products=products)


@app.route('/trousers')
def trousers():
    return '''fsfds'''


@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    form = AddProduct()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        product = Products(
            title=form.title.data,
            content=form.content.data,
            price=form.price.data,
            category=form.category.data,
            user_id=current_user.id,
            image=form.image.data
        )
        db_sess.add(product)
        db_sess.commit()
        return redirect('/home')
    return render_template('add_product.html', title='Добавьте новый продукт', form=form)


@app.route('/basket')
def basket():
    db_sess = db_session.create_session()
    liked = db_sess.query(Liked).filter(Liked.user_id == current_user.id)
    return render_template('basket.html', liked=liked)


@app.route('/logout')
def logout():
    logout_user()
    return redirect("/")


if __name__ == '__main__':
    main()
