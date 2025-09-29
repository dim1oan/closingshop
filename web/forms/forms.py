from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, EmailField, BooleanField, FileField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    gender = StringField('Ваш пол(Мужской/Женский)', validators=[DataRequired()])
    is_invite = BooleanField('Вас пригласили?')
    user_invite = StringField('Код приглашения')
    submit = SubmitField('Зарегистрироваться')


class LoginForm(FlaskForm):
    email = EmailField('Почта / логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Выбрать')


class ChangeLogin(FlaskForm):
    login = StringField('Ваш логин?', validators=[DataRequired()])
    submit = SubmitField('Выбрать')


class ChangeSity(FlaskForm):
    sity = StringField('Ваш город?(Тольятти/Москва)', validators=[DataRequired()])
    submit = SubmitField('Выбрать')


class ChangeGender(FlaskForm):
    gender = StringField('Ваш пол?(Мужской/Женский)', validators=[DataRequired()])
    submit = SubmitField('Выбрать')


class ChangeProductInterest(FlaskForm):
    product_interest = StringField('Интересующие вас товары?(Футболки, обувь, штаны) Пример: "Футболки"', validators=[DataRequired()])
    submit = SubmitField('Выбрать')


class BalanceIn(FlaskForm):
    money = StringField('Сколько хотите пополнить(пишите в цифрах)?', validators=[DataRequired()])
    submit = SubmitField('Выбрать')


class BalanceOut(FlaskForm):
    money = StringField('Сколько хотите вывести(пишите в цифрах)?', validators=[DataRequired()])
    submit = SubmitField('Выбрать')


class AddItem(FlaskForm):
    name = StringField('Название товара', validators=[DataRequired()])
    img = StringField('Название файла с картинкой', validators=[DataRequired()])
    price = StringField('Цена', validators=[DataRequired()])
    price_down = StringField('Скидка', validators=[DataRequired()])
    size = StringField('Какой размер', validators=[DataRequired()])
    count = StringField('В каком количестве', validators=[DataRequired()])
    type_wear = StringField('Тип одежды', validators=[DataRequired()])
    submit = SubmitField('Выбрать')


class ChangePassword(FlaskForm):
    current_password = PasswordField('Ваш текущий пароль', validators=[DataRequired()])
    new_password = PasswordField('Введите новый пароль', validators=[DataRequired()])
    new_password_again = PasswordField('Повторите новый пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')


class AddStore(FlaskForm):
    address = StringField('Адрес в городе', validators=[DataRequired()])
    sity = StringField('Город', validators=[DataRequired()])
    update = StringField('День завоза', validators=[DataRequired()])
    submit = SubmitField('Выбрать')

