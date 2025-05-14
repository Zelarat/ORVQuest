import click
from flask import Blueprint
from flask import cli

bp = Blueprint('cli', __name__, cli_group=None)


@bp.cli.command('show-users')
def show_users():
    """Показать всех пользователей"""
    from app.models import User
    users = User.query.all()
    for u in users:
        print(f"{u.id}: {u.username} ({u.email})")
        
@bp.cli.command('show-quest')
def show_quest():
    from app.models import Task
    quest = Task.query.all()
    for q in quest:
        print(f"{q.id}: {q.quest_name}, {q.question}, {q.task_type}, {q.points}, {q.create_at}, {q.author}, {q.options}")
    
@bp.cli.command('show-questOptions')
def show_quest_optinos():
    from app.models import TaskOption
    quest = TaskOption.query.all()
    for q in quest:
        print(f"{q.id}: {q.task_id}, {q.options}, {q.task}") 