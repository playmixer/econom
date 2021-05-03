from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, FloatField, SelectField, SubmitField
from wtforms.fields.html5 import DateTimeLocalField, DateField
from wtforms.validators import DataRequired, Optional, Length
from datetime import datetime


class Wallet(FlaskForm):
    title = StringField('Название',
                        validators=[DataRequired(), Length(min=4, message="Длина должна быть больше 4 символов")])
    balance = FloatField('Баланс', validators=[Optional()])


class Expense(FlaskForm):
    title = StringField('Наименование', validators=[DataRequired()])
    money = FloatField('Сумма', validators=[DataRequired()])
    wallet_id = SelectField('Счет', validators=[DataRequired()])
    time_event = DateField('Когда', validators=[DataRequired()],
                           default=datetime.now, format='%Y-%m-%d')


class Income(Expense):
    pass


class Yes(FlaskForm):
    submit = SubmitField('Да')
