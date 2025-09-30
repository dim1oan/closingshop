from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    id1 = StringField('Id астронавта', validators=[DataRequired()])
    password1 = PasswordField('Пароль астронавта', validators=[DataRequired()])
    id2 = StringField('Id капитана', validators=[DataRequired()])
    password2 = PasswordField('Пароль капитана', validators=[DataRequired()])
    submit = SubmitField('Доступ')


class PhotoForm(FlaskForm):
    photo = FileField('Загрузи фото')
    submit = SubmitField('Submit')
