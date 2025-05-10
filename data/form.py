from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, EmailField, BooleanField, TimeField
from wtforms.fields.choices import SelectField
from wtforms.validators import DataRequired, Length, ValidationError


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
    submit = SubmitField('Подтвердить')


class SearchFilter(FlaskForm):
    min_price = StringField('Минимальная цена', validators=[DataRequired()])
    max_price = StringField('Максимальная цена', validators=[DataRequired()])
    category = SelectField("Категория", choices=['Футболки', 'Свитшоты', 'Толстовки', 'Брюки', 'Джинсы',
                                                 'Кроссовки', 'Туфли', 'Головные уборы', 'Бижутерия'],
                           validators=[DataRequired()])
    submit = SubmitField('Отфильтровать')


class MakeAnOrder(FlaskForm):
    address = StringField('Адрес доставки', validators=[DataRequired()])
    size = SelectField('Размер', choices=['XXS', 'XS', 'S', 'M', 'L', 'XL'])
    time = TimeField('Время доставки')
    is_delivery_paid = BooleanField('Экспресс-доставка: ')
    payment_method = SelectField('Способ оплаты', choices=['Наличными', 'По карте'])
    submit = SubmitField('Оформить заказ')


class AddCard(FlaskForm):
    number = StringField('Номер',
                         validators=[DataRequired(), Length(min=16, max=16, message=None)])

    def validate_number(form, field):
        if not field.data.isdigit():
            raise ValidationError('Введите корректный номер карты')

    expiration_date = StringField('Срок действия', validators=[DataRequired(), Length(min=4, max=4,
                                                                                      message=None)])

    def validate_expiration_date(form, field):
        if not field.data.isdigit():
            raise ValidationError("Введите корректный срок действия карты")

    cvc = StringField('CVC', validators=[DataRequired(), Length(min=3, max=3,
                                                                message=None)])

    def validate_cvc(form, field):
        if not field.data.isdigit():
            raise ValidationError("Введите корректный CVC карты")

    submit = SubmitField('Подтвердить')


class Balance(FlaskForm):
    balance = StringField('Укажите сумму списания:', validators=[DataRequired()])

    def validate_balance(form, field):
        if not field.data.isdigit():
            raise ValidationError('Введите корректную сумму')

    submit = SubmitField('Подтвердить')


class MakeReview(FlaskForm):
    review = TextAreaField('Напишите отзыв о данном продукте: ', validators=[DataRequired()])
    submit = SubmitField('Подтвердить')
