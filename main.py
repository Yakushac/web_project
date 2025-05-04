from flask import Flask, render_template, make_response, request, redirect, url_for, flash
from data import db_session
from data.db_session import create_session
from data.users import User
from data.products import Products
from data.liked_products import Liked
from data.ordered_products import Ordered
import datetime
from data.login_form import LoginForm, RegisterForm, AddProduct, MakeAnOrder, SearchFilter
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask import abort

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


@app.route('/tshirts')
def tshirts():
    db_sess = db_session.create_session()
    products = db_sess.query(Products).filter(Products.is_private != True, Products.category == 'Футболки')
    return render_template("main_page.html", all_products=products)


@app.route('/sweatshirts')
def sweatshirts():
    db_sess = db_session.create_session()
    products = db_sess.query(Products).filter(Products.is_private != True, Products.category == 'Свитшоты')
    return render_template("main_page.html", all_products=products)


@app.route('/hoodies')
def hoodies():
    db_sess = db_session.create_session()
    products = db_sess.query(Products).filter(Products.is_private != True, Products.category == 'Толстовки')
    return render_template("main_page.html", all_products=products)


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
    products = list(db_sess.query(Products).filter(Products.is_private != True))
    return render_template("main_page.html", all_products=products)


@app.route('/trousers')
def trousers():
    db_sess = db_session.create_session()
    products = db_sess.query(Products).filter(Products.is_private != True, Products.category == 'Брюки')
    return render_template("main_page.html", all_products=products)


@app.route('/jeans')
def jeans():
    db_sess = db_session.create_session()
    products = db_sess.query(Products).filter(Products.is_private != True, Products.category == 'Джинсы')
    return render_template("main_page.html", all_products=products)


@app.route('/sneakers')
def sneakers():
    db_sess = db_session.create_session()
    products = db_sess.query(Products).filter(Products.is_private != True, Products.category == 'Кроссовки')
    return render_template("main_page.html", all_products=products)


@app.route('/shoes')
def shoes():
    db_sess = db_session.create_session()
    products = db_sess.query(Products).filter(Products.is_private != True, Products.category == 'Туфли')
    return render_template("main_page.html", all_products=products)


@app.route('/headdress')
def headdress():
    db_sess = db_session.create_session()
    products = db_sess.query(Products).filter(Products.is_private != True, Products.category == 'Головные уборы')
    return render_template("main_page.html", all_products=products)


@app.route('/jewelry')
def jewerly():
    db_sess = db_session.create_session()
    products = db_sess.query(Products).filter(Products.is_private != True, Products.category == 'Бижутерия')
    return render_template("main_page.html", all_products=products)


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


@app.route('/add_basket', methods=['GET', 'POST'])
def add_basket():
    if request.method == 'POST':
        if current_user.is_authenticated:
            db_sess = db_session.create_session()
            is_have = db_sess.query(Liked).filter(Liked.product_id == request.form.get('id'),
                                                  Liked.user_id == current_user.id).all()
            if not is_have:
                new_liked = Liked(
                    product_id=request.form.get('id'),
                    title=request.form.get('title'),
                    user_id=request.form.get('user_id'),
                    content=request.form.get('content'),
                    price=request.form.get('price'),
                    image=request.form.get('image'),
                    category=request.form.get('category'),
                )
                try:
                    db_sess.add(new_liked)
                    db_sess.commit()
                    return redirect('/')
                except:
                    return redirect('/')
            else:
                return redirect('/notation')
        else:
            return redirect('/notation')


@app.route('/notation')
def notation():
    return render_template("notation.html")


@app.route('/make_an_order/<int:id>', methods=['GET', 'POST'])
@login_required
def make_an_order(id):
    db_sess = db_session.create_session()
    form = MakeAnOrder()

    if request.method == 'POST':
        if current_user.is_authenticated:
            product = db_sess.query(Products).filter(Products.id == id).first()
            address = form.address.data
            time = form.time.data
            size = form.size.data
            is_delivery_paid = form.is_delivery_paid.data
            payment_method = form.payment_method.data

            ordered_item = Ordered(
                product_id=product.id,
                title=product.title,
                price=product.price,
                content=product.content,
                is_private=product.is_private,
                user_id=current_user.id,
                category=product.category,
                image=product.image,
                address=address,
                time=time,
                size=size,
                is_delivery_paid=is_delivery_paid,
                payment_method=payment_method,
                created_date=product.created_date
            )

            db_sess.add(ordered_item)
            db_sess.commit()
            return redirect('/ordered_products')
    return render_template('make_an_order.html', form=form)


@app.route('/cancel_order/<int:id>', methods=['GET', 'POST'])
@login_required
def cancel_order(id):
    db_sess = db_session.create_session()
    products = db_sess.query(Ordered).filter(Ordered.id == id, Ordered.user_id == current_user.id).first()
    if products:
        db_sess.delete(products)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/ordered_products')


@app.route('/delete_product/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_product(id):
    db_sess = db_session.create_session()
    products = db_sess.query(Products).filter(Products.id == id,
                                              Products.user_id == current_user.id
                                              ).first()
    if products:
        db_sess.delete(products)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/home')


@app.route('/edit_product/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_product(id):
    form = AddProduct()
    if request.method == "GET":
        db_sess = db_session.create_session()
        products = db_sess.query(Products).filter(Products.id == id,
                                                  Products.user_id == current_user.id
                                                  ).first()
        if products:
            form.title.data = products.title
            form.content.data = products.content
            form.image.data = products.image
            form.price.data = products.price
            form.category.data = products.category
            form.is_private.data = products.is_private
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        products = db_sess.query(Products).filter(Products.id == id,
                                                  Products.user_id == current_user.id
                                                  ).first()
        if products:
            products.title = form.title.data
            products.image = form.image.data
            products.price = form.price.data
            products.category = form.category.data
            products.content = form.content.data
            products.is_private = form.is_private.data
            db_sess.commit()
            return redirect('/home')
        else:
            abort(404)
    return render_template('add_product.html',
                           title='Изменить сведения о продукте',
                           form=form
                           )


@app.route('/ordered_products')
def ordered_products():
    db_sess = db_session.create_session()
    ordered = db_sess.query(Ordered).filter(Ordered.user_id == current_user.id)
    return render_template('ordered_products.html', ordered=ordered)


@app.route('/search', methods=['GET', 'POST'])
def search():
    form = SearchFilter()
    if request.method == 'POST':
        min_price = form.min_price.data
        max_price = form.max_price.data
        category = form.category.data
        try:
            min_and_max = " ".join([min_price, max_price, category])
            return redirect(url_for('filtered', min_and_max=min_and_max))
        except:
            return redirect('/notation')
    return render_template('search.html', form=form)


@app.route('/filtered/<min_and_max>')
def filtered(min_and_max):
    try:
        min_price = int(min_and_max.split(' ')[0])
        max_price = int(min_and_max.split(' ')[1])
        category = min_and_max.split(' ')[2]
        db_sess = db_session.create_session()
        filtered_products = db_sess.query(Products).filter(Products.price >= min_price,
                                                           Products.price <= max_price, Products.category == category).all()
        return render_template('main_page.html', all_products=filtered_products)
    except:
        return render_template('/notation')

@app.route('/logout')
def logout():
    logout_user()
    return redirect("/")


if __name__ == '__main__':
    main()
