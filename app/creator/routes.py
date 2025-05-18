from flask import render_template, redirect, url_for, flash, request, jsonify, json, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os
from app.creator import bp as creator_bp
from app.creator.forms import SearchQuestions
from app import db
from app.models import Task
from sqlalchemy import or_


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']


@creator_bp.before_request
@login_required
def before_request():
    if not current_user.is_admin:
        flash('Доступ запрещен', 'danger')
        return redirect(url_for('main.index'))

@creator_bp.route('/creator')
def tasks():
    search_form = SearchQuestions()
    questions = Task.query.all()
    print(request.form)
    if search_form.validate_on_submit():
        if search_form.cancel.data:
            return render_template('creator/tasks.html', title="Задания",
                                   search_form=search_form,
                                   tasks=questions)
        
        search_name = search_form.questions_name.data
        search_author = search_form.questions_author.data
        
        query = Task.query
        
        filters = []
        if search_name:
            filters.append(Task.quest_name.ilike(f"%{search_name}%"))
        if search_author:
            filters.append(Task.author.ilike(f"%{search_author}%"))
            
        if filters:
            questions = query.filter(or_(*filters))
        else:
            questions = query.all()
        
        return render_template('creator/tasks.html', title='Задания',
                           search_form=search_form,
                           tasks=questions)
        
    return render_template('creator/tasks.html', title='Задания',
                           search_form=search_form,
                           tasks=questions)

@creator_bp.route('/constructor')
@login_required
def constructor():
    return render_template('creator/constructor.html', title="Конструктор заданий")

@creator_bp.route('/get_widgets', methods=['POST'])
@login_required
def get_widgets():
    data = request.json
    widgets = data.get('widgets', [])
    print(data)
    print(widgets)
    options = []
    points = []
    answer = []
    result = []
    
    for widget in widgets:
        
        if widget["type"] == "written_answer":
            points.append(widget["points"])
            options.append({
                "type": widget["type"],
                "description": widget["question"].lower()
                })
            if widget["data"]["server_check"]:
                answer.append(widget["data"]["correct_answer"])

        elif widget["type"] == "select":
            points.append(widget["points"])
            options.append({
                "type": widget["type"],
                "description": widget["question"],
                "options": []
                })
            for option in widget["data"]["options"]:
                options[-1]["options"].append(option["text"])
                if option["is_correct"]:
                    answer.append(option["text"])

        elif widget["type"] == "checkbox":
            points.append(widget["points"])
            options.append({
                "type": widget["type"],
                "description": widget["question"],
                "options": []
                })
            for option in widget["data"]["options"]:
                options[-1]["options"].append(option["text"])
                if option["is_correct"]:
                    answer.append(option["text"])

        elif widget["type"] == "file":
            points.append(widget["points"])
            options.append({
                "type": widget["type"],
                "options": []
            })
            for file in widget["data"]["files"]:
                filedata = request.files.get(file["file"])
                
                
    
    print(options)
    print(points)
    print(answer)
        
    return jsonify(result)