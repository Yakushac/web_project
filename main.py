from flask import Flask, render_template, make_response, request, redirect, url_for, flash
from data import db_session
from data.db_session import create_session
from data.users import User
from data.products import Products
from data.liked_products import Liked
from data.ordered_products import Ordered
from data.cards import Cards
from data.reviews import Reviews
from data.login_form import LoginForm, RegisterForm, AddProduct, MakeAnOrder, SearchFilter, AddCard, Balance, MakeReview
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
    if current_user.is_authenticated:
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
def register():
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
@login_required
def home():
    db_sess = db_session.create_session()
    products = db_sess.query(Products).filter(Products.user_id == current_user.id).all()
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
@login_required
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
@login_required
def basket():
    db_sess = db_session.create_session()
    liked = db_sess.query(Liked).filter(Liked.user_id == current_user.id).all()
    return render_template('basket.html', liked=liked)


@app.route('/add_basket/<int:id>', methods=['GET', 'POST'])
@login_required
def add_basket(id):
    if current_user.is_authenticated:
        db_sess = db_session.create_session()
        is_have = db_sess.query(Liked).filter(Liked.product_id == id,
                                              Liked.user_id == current_user.id).first()
        product = db_sess.query(Products).filter(Products.id == id).first()
        if not is_have:
            new_liked = Liked(
                product_id=id,
                title=product.title,
                user_id=current_user.id,
                content=product.content,
                price=product.price,
                image=product.image,
                category=product.category,
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


@app.route('/delete_basket/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_basket(id):
    db_sess = db_session.create_session()
    product = db_sess.query(Liked).filter(Liked.id == id, Liked.user_id == current_user.id).first()
    if product:
        db_sess.delete(product)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/basket')


@app.route('/notation')
def notation():
    return render_template("notation.html")


@app.route('/make_an_order/<int:id>', methods=['GET', 'POST'])
@login_required
def make_an_order(id):
    db_sess = db_session.create_session()
    form = MakeAnOrder()

    if request.method == 'POST':
        if form.validate_on_submit():
            product = db_sess.query(Products).filter(Products.id == id).first()
            user = db_sess.query(User).filter(User.id == current_user.id).first()
            if current_user.balance >= product.price:
                user.balance = user.balance - product.price
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
            else:
                return '''Недостаточно средств. Пополните баланс и сделайте заказ заново.'''
    return render_template('make_an_order.html', form=form)


@app.route('/reviews/<int:id>')
def reviews(id):
    db_sess = db_session.create_session()
    reviews = db_sess.query(Reviews).filter(Reviews.product_id == id).all()
    product = db_sess.query(Products).filter(Products.id == id).first()
    return render_template('view_reviews.html', reviews=reviews, product=product)


@app.route('/cancel_order/<int:id>')
@login_required
def cancel_order(id):
    db_sess = db_session.create_session()
    products = db_sess.query(Ordered).filter(Ordered.id == id, Ordered.user_id == current_user.id).first()
    user = db_sess.query(User).filter(User.id == current_user.id).first()
    if products:
        user.balance = user.balance + products.price
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
                           form=form)


@app.route('/ordered_products')
@login_required
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
                                                           Products.price <= max_price,
                                                           Products.category == category).all()
        return render_template('main_page.html', all_products=filtered_products)
    except:
        return render_template('/notation')


@app.route('/wallet')
@login_required
def wallet():
    db_sess = db_session.create_session()
    cards = db_sess.query(Cards).filter(Cards.user_id == current_user.id).all()
    print(cards)
    return render_template('wallet.html', your_cards=cards)


@app.route('/edit_card/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_card(id):
    form = AddCard()
    if request.method == 'GET':
        db_sess = db_session.create_session()
        card = db_sess.query(Cards).filter(Cards.id == id, Cards.user_id == current_user.id).first()
        if card:
            form.number.data = card.number
            form.expiration_date.data = card.expiration_date
            form.cvc.data = card.cvc
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        card = db_sess.query(Cards).filter(Cards.id == id, Cards.user_id == current_user.id).first()
        if card:
            card.number = form.number.data
            card.expiration_date = form.expiration_date.data
            card.cvc = form.cvc.data
            db_sess.commit()
            return redirect('/wallet')
        else:
            abort(404)
    return render_template('add_card.html',
                           title='Изменить сведения о карте', form=form)


@app.route('/delete_card/<int:id>')
@login_required
def delete_card(id):
    db_sess = db_session.create_session()
    card = db_sess.query(Cards).filter(Cards.id == id, Cards.user_id == current_user.id).first()
    if card:
        db_sess.delete(card)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/wallet')


@app.route('/add_card', methods=['GET', 'POST'])
@login_required
def add_card():
    form = AddCard()
    if request.method == 'POST':
        if form.validate_on_submit():
            db_sess = db_session.create_session()
            if_cards = db_sess.query(Cards).filter(Cards.number == form.number.data,
                                                   Cards.user_id == current_user.id).all()
            if not if_cards:
                new_card = Cards(
                    number=form.number.data,
                    expiration_date=form.expiration_date.data,
                    cvc=form.cvc.data,
                    user_id=current_user.id
                )
                db_sess.add(new_card)
                db_sess.commit()
                return redirect('/wallet')
            else:
                return '''Такая карта уже добавлена'''
    return render_template('add_card.html', form=form, title='Добавить карту')


@app.route('/top_up_balance/<int:id>', methods=['GET', 'POST'])
@login_required
def top_up_balance(id):
    form = Balance()
    if request.method == 'POST':
        if form.validate_on_submit():
            db_sess = db_session.create_session()
            user = db_sess.query(User).filter(User.id == current_user.id).first()
            user.balance += int(form.balance.data)
            db_sess.commit()
            return redirect('/wallet')
    return render_template('top_up_balance.html', title='Пополнить баланс кошелька', form=form)


@app.route('/make_review/<int:id>', methods=['GET', 'POST'])
@login_required
def make_review(id):
    id = id
    form = MakeReview()
    db_sess = db_session.create_session()
    if request.method == 'POST':
        if form.validate_on_submit():
            new_review = Reviews(
                product_id=id,
                review=form.review.data,
                user_id=current_user.id
            )
            db_sess.add(new_review)
            db_sess.commit()
            return redirect(url_for('reviews', id=id))
    return render_template('make_review.html', form=form, title="Оставить отзыв")


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


if __name__ == '__main__':
    main()
