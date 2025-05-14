from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField


class SearchQuestions(FlaskForm):
    questions_name = StringField("Название задания")
    questions_author = StringField("Имя автора")
    search = SubmitField("Поиск")
    cancel = SubmitField("Сбросить")