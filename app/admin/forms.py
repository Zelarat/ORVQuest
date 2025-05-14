from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateTimeLocalField, SelectField, BooleanField, FieldList, FormField, IntegerField, SubmitField, HiddenField, FloatField
from wtforms.validators import DataRequired, Optional, InputRequired, Length, NumberRange

class SearchQuestions(FlaskForm):
    questions_name = StringField("Название задания")
    questions_author = StringField("Имя автора")
    search = SubmitField("Поиск")
    cancel = SubmitField("Сбросить")
    
class ModalCreateQuest(FlaskForm):
    select_quest_type = SelectField("Тип задания", choices=[
        ('create_single', 'Одиночный выбор'),
        ('create_multi', 'Множественный выбор'),
        ('create_text', 'Текстовый ответ'),
        ('create_integer', 'Числовой ответ')
    ], validators=[DataRequired()])
    submit = SubmitField("Создать")

class AnswerOptionForm(FlaskForm):
    text = StringField('Текст варианта', validators=[DataRequired()])
    is_correct = BooleanField('Правильный ответ', default=False)
    
class CreateSingleOrMultiForm(FlaskForm):
    quest_name = StringField("Название задания", validators=[DataRequired()])
    quest_description = TextAreaField("Условие задания", validators=[DataRequired()])
    quest_points = IntegerField("Баллы за задание", validators=[DataRequired()])
    quest_options = FieldList(FormField(AnswerOptionForm), min_entries=1)
    submit = SubmitField("Создать")
    edit = SubmitField("Изменить")

class CreateTextForm(FlaskForm):
    quest_name = StringField("Название задания", validators=[DataRequired()])
    quest_description = TextAreaField("Условие задания", validators=[DataRequired()])
    quest_points = IntegerField("Баллы за задание", validators=[DataRequired()])
    quest_options = StringField("Правильный ответ")
    quest_setting = BooleanField("Проверка комиссией")
    submit = SubmitField("Создать")
    edit = SubmitField("Изменить")

class CreateIntegerForm(FlaskForm):
    quest_name = StringField("Название задания", validators=[DataRequired()])
    quest_description = TextAreaField("Условие задания", validators=[DataRequired()])
    quest_points = IntegerField("Баллы за задание", validators=[DataRequired()])
    quest_options = FloatField("Ответ", validators=[DataRequired(), NumberRange(min=0)])
    quest_error_rate = FloatField("Погрешность", validators=[DataRequired(), NumberRange(min=0)])
    submit = SubmitField("Создать")
    edit = SubmitField("Изменить")

class CreateTournament(FlaskForm):
    tour_name = StringField("Название турнира", validators=[DataRequired()])
    tour_description = TextAreaField("Описание турнира", validators=[DataRequired()])
    group_name = StringField("Название группы", validators=[DataRequired()])
    count_quest = IntegerField("Задание для прохождения группы", validators=[DataRequired()])
    
    
#Старьё
class AssignmentForm(FlaskForm):
    title = StringField('Название задания', validators=[DataRequired()])
    description = TextAreaField('Описание')
    deadline = DateTimeLocalField('Срок выполнения', format='%Y-%m-%dT%H:%M')
    form_id = SelectField('Связанная форма', coerce=int)
    is_active = BooleanField('Активное задание')
    


class QuestionForm(FlaskForm):
    QUESTION_TYPES = [
        ('Одиночный выбор', 'Одиночный выбор'),
        ('Множественный выбор', 'Множественный выбор'),
        ('Текстовый ответ', 'Текстовый ответ'),
        ('Числовой ответ', 'Числовой ответ')
    ]
    
    assignment_name = StringField('Имя задания', validators=[DataRequired()])
    question_type = SelectField('Тип вопроса', choices=QUESTION_TYPES, validators=[DataRequired()])
    text = TextAreaField('Текст вопроса', validators=[DataRequired()])
    points = IntegerField('Баллы', default=1, validators=[DataRequired()])
    options = FieldList(FormField(AnswerOptionForm), min_entries=1)
    correct_text_answer = StringField('Правильный текстовый ответ', validators=[Optional()])
    correct_number_answer = IntegerField('Правильный числовой ответ', validators=[Optional()])
    submit = SubmitField('Сохранить задание')

class CreateTournamentForm(FlaskForm):
    tour_name = StringField('Название турнира', validators=[DataRequired()])
    description = StringField('Описание турнира', validators=[DataRequired()])
    time_to_tour = IntegerField('Длительность турнира (в минутах)', validators=[DataRequired()])

class EntryOptional(FlaskForm):
    castom_points = IntegerField("Изменить баллы за задание", validators=[DataRequired()])
    delete_quest = SubmitField("Удалить задание")
    
class TaskGroupForm(FlaskForm):
    group_name = StringField('Название группы', validators=[DataRequired()])
    display_type = SelectField('Отображение заданий в группе', 
                             choices=[('sequential', 'Последовательно'), 
                                      ('random', 'Случайный порядок')],
                             default='sequential')
    selected_tasks = HiddenField()

class GroupForm(FlaskForm):
    group_name = StringField('Название группы', validators=[DataRequired()])
    display_type = SelectField('Тип отображения', choices=[
        ('list', 'Список'),
        ('random', 'Случайный порядок'),
        ('pagination', 'Постранично')
    ], validators=[DataRequired()])
    selected_tasks = HiddenField('Выбранные задания')

class TournamentForm(FlaskForm):
    tour_name = StringField('Название теста', validators=[DataRequired()])
    tour_description = TextAreaField('Описание теста')
    groups = FieldList(FormField(GroupForm), min_entries=1)