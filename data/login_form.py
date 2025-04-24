from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, EmailField, BooleanField, TimeField
from wtforms.fields.choices import SelectField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class RegisterForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    name = StringField('Имя пользователя', validators=[DataRequired()])
    about = TextAreaField("Немного о себе")
    submit = SubmitField('Войти')


class AddProduct(FlaskForm):
    title = StringField('Название продукта', validators=[DataRequired()])
    content = TextAreaField("Описание", validators=[DataRequired()])
    category = SelectField("Категория", choices=['Футболки', 'Свитшоты', 'Толстовки', 'Брюки', 'Джинсы',
                                                 'Кроссовки', 'Туфли', 'Головные уборы', 'Бижутерия', 'Общее'],
                           validators=[DataRequired()])
    is_private = BooleanField('Сделать продукт приватным:')
    price = StringField('Цена', default='0')
    image = StringField('Ссылка на изображение:', validators=[DataRequired()])
    submit = SubmitField('Добавить')


class MakeAnOrder(FlaskForm):
    address = StringField('Адрес доставки', validators=[DataRequired()])
    size = SelectField('Размер', choices=['XXS', 'XS', 'S', 'M', 'L', 'XL'])
    time = TimeField('Время доставки')
    is_delivery_paid = BooleanField('Экспресс-доставка: ')
    payment_method = SelectField('Способ оплаты', choices=['Наличными', 'По карте'])
    submit = SubmitField('Оформить заказ')
