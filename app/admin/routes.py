from flask import render_template, redirect, url_for, flash, request, jsonify, json
from flask_login import login_required, current_user
from app.models import Task, TaskOption, Tournament, TourResult, TourSetting, NumberAnswer, TextAnswer
from app import db
from datetime import datetime, timezone
from sqlalchemy import or_
from app.admin import bp as admin_bp
from app.admin.forms import SearchQuestions, ModalCreateQuest, CreateIntegerForm, CreateTextForm, CreateSingleOrMultiForm, AnswerOptionForm, CreateTournament
import sqlalchemy.orm as so


@admin_bp.before_request
@login_required
def before_request():
    if not current_user.is_admin:
        flash('Доступ запрещен', 'danger')
        return redirect(url_for('main.index'))

@admin_bp.route('/questions', methods=["GET", "POST"])
@login_required
def questions():
    search_form = SearchQuestions()
    modal_form = ModalCreateQuest()
    questions = Task.query.all()
    print(request.form)
    if search_form.validate_on_submit():
        print("YES")
        if search_form.cancel.data:
            return render_template('admin/questions.html', title="Задания",
                                   search_form=search_form,
                                   modal_form=modal_form,
                                   tasks=questions)
        
        search_name = search_form.questions_name.data
        search_type = search_form.questions_type.data
        search_author = search_form.questions_author.data
        
        query = Task.query
        
        filters = []
        if search_name:
            filters.append(Task.quest_name.ilike(f"%{search_name}%"))
        if search_type:
            filters.append(Task.task_type.ilike(f"%{search_type}%"))
        if search_author:
            filters.append(Task.author.ilike(f"%{search_author}%"))
        
        if filters:
            questions = query.filter(or_(*filters))
        else:
            questions = query.all()
        
        return render_template('admin/questions.html', title='Задания',
                           search_form=search_form,
                           modal_form=modal_form,
                           tasks=questions)
    
    
    
    return render_template('admin/questions.html', title='Задания',
                           search_form=search_form,
                           modal_form=modal_form,
                           tasks=questions)
    
@admin_bp.route('/select_quest_type_create', methods=["GET", "POST"])
@login_required
def select_quest_type_create():
    modal_form = ModalCreateQuest()
    if modal_form.validate_on_submit():
        print(modal_form.select_quest_type.data)
        return redirect(url_for(f'admin.{modal_form.select_quest_type.data}'))
    
@admin_bp.route('/create_single', methods=["GET", "POST"])
@login_required
def create_single():
    form = CreateSingleOrMultiForm(formdata=request.form)
    print(form.errors)
    print(request.form)
    if form.validate_on_submit():
        correct_count = sum(1 for option in form.quest_options.data if option['is_correct'])
        
        if correct_count > 1:
            flash('Может быть только один правильный ответ', 'danger')
            return render_template('admin/create/create_single.html', form=form)
        elif correct_count < 1:
            flash('Выберите правильный ответ', 'danger')
            return render_template('admin/create/create_single.html', form=form)

        try:
            # Создаем новую запись задания
            new_task = Task(
                quest_name=form.quest_name.data,
                question=form.quest_description.data,  # предполагая, что это текст вопроса
                task_type='Одиночный выбор',  # или другой тип из вашей логики
                points=form.quest_points.data,
                author=current_user.username,  # предполагая использование Flask-Login
                create_at=datetime.now(timezone.utc)
            )

            # Добавляем в сессию
            db.session.add(new_task)
            db.session.flush()  # Получаем ID для связей

            # Подготавливаем варианты ответов
            options_data = [
                {"text": option["text"], "is_correct": option["is_correct"]}
                for option in form.quest_options.data
            ]
            print(options_data)
            # Создаем запись вариантов ответов
            task_options = TaskOption(
                task_id=new_task.id,
                options=options_data
            )
            
            db.session.add(task_options)
            db.session.commit()
            
            return redirect(url_for("admin.questions"))

        except Exception as e:
            db.session.rollback()
            flash(f'Ошибка при создании задания: {str(e)}', 'danger')

    return render_template('admin/create/create_single.html', form=form)

@admin_bp.route('/create_multi', methods=["GET", "POST"])
@login_required
def create_multi():
    form = CreateSingleOrMultiForm()
    if form.validate_on_submit():
        correct_count = sum(1 for option in form.quest_options.data if option['is_correct'])
        
        if correct_count < 1:
            flash('Добавьте правильный ответ', 'danger')
            return render_template('admin/create/create_multi.html', form=form)
        
        try:
            # Создаем новую запись задания
            new_task = Task(
                quest_name=form.quest_name.data,
                question=form.quest_description.data,
                task_type='Множественный выбор',
                points=form.quest_points.data,
                author=current_user.username,
                create_at=datetime.now(timezone.utc)
            )

            db.session.add(new_task)
            db.session.flush()

            options_data = [
                {"text": option["text"], "is_correct": option["is_correct"]}
                for option in form.quest_options.data
            ]

            task_options = TaskOption(
                task_id=new_task.id,
                options=options_data
            )
            
            db.session.add(task_options)
            db.session.commit()
            
            return redirect(url_for("admin.questions"))

        except Exception as e:
            db.session.rollback()
            flash(f'Ошибка при создании задания: {str(e)}', 'danger')
        
    return render_template('admin/create/create_multi.html', title='Создание задания', form=form)

@admin_bp.route('/create_text', methods=["GET", "POST"])
@login_required
def create_text():
    form = CreateTextForm()
    print(form.errors)
    if form.validate_on_submit():
        try:
            # Создаем новую запись задания
            new_task = Task(
                quest_name=form.quest_name.data,
                question=form.quest_description.data,
                task_type='Текстовый ответ',
                points=form.quest_points.data,
                author=current_user.username,
                create_at=datetime.now(timezone.utc)
            )

            db.session.add(new_task)
            db.session.flush()
            
            if form.quest_setting.data:
                quest_text = None
            else:
                quest_text = form.quest_options.data
            
            task_answer = TextAnswer(
                task_id=new_task.id,
                text_answer=quest_text,
                is_regular=form.quest_setting.data
            )
            
            db.session.add(task_answer)
            db.session.commit()
            
            return redirect(url_for("admin.questions"))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Ошибка при создании задания: {str(e)}', 'danger')
        
    return render_template('admin/create/create_text.html', title='Создание задания', form=form)

@admin_bp.route('/create_integer', methods=["GET", "POST"])
@login_required
def create_integer():
    form = CreateIntegerForm()
    print(request.form)
    print(form.errors)
    if form.validate_on_submit():
        try:
            
            # Создаем новую запись задания
            new_task = Task(
                quest_name=form.quest_name.data,
                question=form.quest_description.data,
                task_type='Числовой ответ',
                points=form.quest_points.data,
                author=current_user.username,
                create_at=datetime.now(timezone.utc)
            )

            db.session.add(new_task)
            db.session.flush()
            
            task_answer = NumberAnswer(
                task_id=new_task.id,
                answer=form.quest_options.data,
                error_rate=form.quest_error_rate.data
            )
            
            db.session.add(task_answer)
            db.session.commit()
            
            return redirect(url_for("admin.questions"))
                        
        except Exception as e:
            db.session.rollback()
            flash(f'Ошибка при создании задания: {str(e)}', 'danger')
            
    return render_template('admin/create/create_integer.html', title='Создание задания', form=form)

@admin_bp.route('/tasks/<int:task_id>/view')
@login_required
def view_task(task_id):
    task = Task.query.get_or_404(task_id)
    return render_template('admin/view_task.html', task=task)

@admin_bp.route('/tasks/<int:task_id>/edit')
@login_required
def edit_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.task_type == "Одиночный выбор":
        return redirect(url_for("admin.edit_single", task_id=task_id))
    elif task.task_type == "Множественный выбор":
        return redirect(url_for(f"admin.edit_multi", task_id=task_id))
    elif task.task_type == "Текстовый ответ":
        return redirect(url_for(f"admin.edit_text", task_id=task_id))
    elif task.task_type == "Числовой ответ":
        return redirect(url_for(f"admin.edit_integer", task_id=task_id))


@admin_bp.route('/edit_single/<int:task_id>', methods=["GET", "POST"])
@login_required
def edit_single(task_id):
    if request.method == 'POST':
        form_data = request.form.to_dict()
        
        # Добавляем False для отсутствующих чекбоксов
        i = 0
        while f'quest_options-{i}-text' in form_data:
            if f'quest_options-{i}-is_correct' not in form_data:
                form_data[f'quest_options-{i}-is_correct'] = 'false'
            i += 1
        
        # Создаем форму с модифицированными данными
        from werkzeug.datastructures import ImmutableMultiDict
        form = CreateSingleOrMultiForm(formdata=ImmutableMultiDict(form_data))
    else:
        form = CreateSingleOrMultiForm()
    
    task = Task.query.get_or_404(task_id)
    #form = CreateSingleOrMultiForm(formdata=request.form)
    form.quest_name.data = task.quest_name
    form.quest_description.data = task.question
    form.quest_points.data = task.points
    options = task.options.options
    form.quest_options.entries = []
    for option in options:
        entry = form.quest_options.append_entry()
        entry.text.data = option["text"]
        entry.is_correct.data = option["is_correct"]
    print(form.errors)
    print(request.form)
    if form.validate_on_submit():
        try:
            correct_count = sum(1 for option in form.quest_options.data if option['is_correct'])
            
            if correct_count > 1:
                flash('Может быть только один правильный ответ', 'danger')
                return render_template("admin/edit/edit_single.html", title="Редактирование", form=form, task_id=task_id)
            elif correct_count < 1:
                flash('Выберите правильный ответ', 'danger')
                return render_template("admin/edit/edit_single.html", title="Редактирование", form=form, task_id=task_id)
            
            task = db.session.get(Task, task_id)
            
            task.quest_name = form.quest_name.data
            task.question = form.quest_description.data
            task.points = form.quest_points.data
            
            task.options.options = [
                    {"text": option["text"], "is_correct": option["is_correct"]}
                    for option in form.quest_options.data
                ]
            
            db.session.commit()
            return redirect(url_for("admin.questions"))
        
        except Exception as e:
            db.session.rollback()
            flash(f'Ошибка при создании задания: {str(e)}', 'danger')
    
    return render_template("admin/edit/edit_single.html", title="Редактирование", form=form, task_id=task_id)

@admin_bp.route('/edit_multi/<int:task_id>', methods=["GET", "POST"])
@login_required
def edit_multi(task_id):
    task = Task.query.get_or_404(task_id)
    form = CreateSingleOrMultiForm()
    form.quest_name.data = task.quest_name
    form.quest_description.data = task.question
    form.quest_points.data = task.points
    options = task.options.options
    form.quest_options.entries = []
    for option in options:
        entry = form.quest_options.append_entry()
        entry.text.data = option["text"]
        entry.is_correct.data = option["is_correct"]
    
    if form.validate_on_submit():
        correct_count = sum(1 for option in form.quest_options.data if option['is_correct'])
        
        if correct_count < 1:
            flash('Выберите правильный ответ', 'danger')
            return render_template("admin/edit/edit_multi.html", title="Редактирование", form=form, task_id=task_id)
        
        task = db.session.get(Task, task_id)
        
        task.quest_name = form.quest_name.data
        task.question = form.quest_description.data
        task.points = form.quest_points.data
        
        task.options.options = [
                {"text": option["text"], "is_correct": option["is_correct"]}
                for option in form.quest_options.data
            ]
        
        db.session.commit()
        return redirect(url_for("admin.questions"))
    
    return render_template("admin/edit/edit_multi.html", title="Редактирование", form=form, task_id=task_id)

@admin_bp.route('/edit_text/<int:task_id>', methods=["GET", "POST"])
@login_required
def edit_text(task_id):
    task = Task.query.get_or_404(task_id)
    form = CreateTextForm()
    form.quest_name.data = task.quest_name
    form.quest_description.data = task.question
    form.quest_points.data = task.points
    form.quest_options.data = task.text_answer.text_answer
    form.quest_setting.data = task.text_answer.is_regular
    
    if form.validate_on_submit():
        task.quest_name = form.quest_name.data
        task.question = form.quest_description.data
        task.points = form.quest_points.data
        task.text_answer.text_answer = form.quest_options.data
        task.text_answer.is_regular = form.quest_setting.data
    
        db.session.commit()
        
        return redirect(url_for("admin.questions"))
    return render_template("admin/edit/edit_text.html", title="Редактирование", form=form, task_id=task_id)
    
@admin_bp.route('/edit_integer/<int:task_id>', methods=["GET", "POST"])
@login_required
def edit_integer(task_id):
    task = Task.query.get_or_404(task_id)
    form = CreateIntegerForm()
    form.quest_name.data = task.quest_name
    form.quest_description.data = task.question
    form.quest_points.data = task.points
    form.quest_options.data = task.number_answer.answer
    form.quest_error_rate.data = task.number_answer.error_rate
    
    if form.validate_on_submit():
        task.quest_name = form.quest_name.data
        task.question = form.quest_description.data
        task.points = form.quest_points.data
        task.number_answer.answer = form.quest_options.data
        task.number_answer.error_rate = form.quest_error_rate.data
        
        db.session.commit()
        
        return redirect(url_for("admin.questions"))
    return render_template("admin/edit/edit_integer.html", title="Редактирование", form=form, task_id=task_id)

@admin_bp.route('/tasks/<int:task_id>/delete', methods=['POST'])
@login_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return jsonify({'success': True}), 200

@admin_bp.route('/create_tour', methods=["GET", "POST"])
@login_required
def create_tour():
    search_form = SearchQuestions()
    form = CreateTournament()
    tasks = Task.query.all()
    return render_template('admin/create/create_tournament.html',
                         search_form=search_form,
                         form=form,
                         tasks=tasks)

@admin_bp.route('/select_quest_tour', methods=["GET", "POST"])
@login_required
def select_quest_tour():
    search_form = SearchQuestions()
    form = CreateTournament()
    query = Task.query
    
    # Обработка AJAX-запроса (поиск или сброс)
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        # Если нажата кнопка "Сбросить"
        if 'cancel' in request.form:
            tasks = Task.query.all()  # Получаем все задачи без фильтров
        else:
            # Обычный поиск
            if search_form.validate():
                search_name = search_form.questions_name.data
                search_type = search_form.questions_type.data
                search_author = search_form.questions_author.data
                
                filters = []
                if search_name:
                    filters.append(Task.quest_name.ilike(f"%{search_name}%"))
                if search_type:
                    filters.append(Task.task_type.ilike(f"%{search_type}%"))
                if search_author:
                    filters.append(Task.author.ilike(f"%{search_author}%"))
                
                if filters:
                    query = query.filter(or_(*filters))
            
            tasks = query.all()
        
        return render_template('admin/create/_tasks_table.html', 
                            search_form=search_form, 
                            form=form, 
                            tasks=tasks)
    
    # Обычный GET-запрос (первоначальная загрузка)
    tasks = Task.query.all()
    return render_template('admin/create/create_tournament.html',
                         search_form=search_form,
                         form=form,
                         tasks=tasks)
    
@admin_bp.route('/reset_search', methods=["GET"])
@login_required
def reset_search():
    tasks = Task.query.all()
    return render_template('admin/create/_tasks_table.html', 
                         tasks=tasks,
                         search_form=SearchQuestions(),
                         form=CreateTournament())
            
@admin_bp.route('/save_selected_task', methods=['POST'])
@login_required
def save_selected_task():
    try:
        if not request.is_json:
            print("error")
            return jsonify({'success': False, 'message': 'Неверный формат запроса'}), 400
        print("NICE")
        data = request.get_json()
        selected_ids = data.get('selected_tasks', [])
        print(selected_ids)
        
        if not selected_ids:
            return jsonify({'success': False, 'message': 'Не выбрано ни одного задания'}), 400
        
        # Преобразуем ID в числа и проверяем их существование
        task_ids = []
        for task_id in selected_ids:
            try:
                task_ids.append(int(task_id))
            except (ValueError, TypeError):
                continue
        
        # Получаем задания из БД
        selected_tasks = Task.query.filter(Task.id.in_(task_ids)).all()
        print(selected_tasks)
        # Сохраняем выбранные задания (пример)
        # Здесь можно сохранить в сессии, БД или выполнить другие действия
        #session['selected_tasks'] = [task.id for task in selected_tasks]
        
        return jsonify({
            'success': True,
            'message': f'Выбрано {len(selected_tasks)} заданий',
            'selected_ids': [task.id for task in selected_tasks]
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Ошибка сервера: {str(e)}'
        }), 500