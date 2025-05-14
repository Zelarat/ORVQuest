from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from email_validator import validate_email, EmailNotValidError
from app import db
from app.models import Users
import sqlalchemy as sa


class LoginForm(FlaskForm):
    username = StringField("Логин", validators=[DataRequired()])
    password = PasswordField("Пароль", validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')
    

class RegistrationForm(FlaskForm):
    username = StringField("Логин", validators=[DataRequired(), Length(min=4, max=64)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Пароль", validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField(
        "Подтвердите пароль", validators=[DataRequired(), EqualTo('password', message="Пароли не совпадают")]
    )
    submit1 = SubmitField('Далее')
    name = StringField("Имя", validators=[DataRequired(), Length(max=32)])
    second_name = StringField("Фамилия", validators=[DataRequired(), Length(max=32)])
    patronymic = StringField("Отчество", validators=[Length(max=32)])
    place_of_work = StringField("Место работы", validators=[Length(max=64)])
    position = StringField("Должность", validators=[Length(max=64)])
    submit = SubmitField('Зарегистрироваться')
    
    def validate_username(self,username):
        user = db.session.scalar(sa.select(Users).where(
            Users.username == username.data
        ))
        if user is not None:
            raise ValidationError('Имя пользователя занято.')
    
    def validate_email(self, email):
        user = db.session.scalar(sa.select(Users).where(
            Users.email == email.data
        ))
        if user is not None:
            raise ValidationError('Эта почта уже зарегистрирована.')
