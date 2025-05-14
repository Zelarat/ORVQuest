from flask import render_template, redirect, url_for, flash, request, jsonify, json
from app.creator import bp
from app.creator.forms import SearchQuestions
from app import db
from app.models import Task
from sqlalchemy import or_

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