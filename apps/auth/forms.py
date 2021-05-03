from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Optional, Length


class FormLogin(FlaskForm):
    username = StringField('Пользователь', validators=[Optional()])
    password = PasswordField('Пароль', validators=[Optional()])
