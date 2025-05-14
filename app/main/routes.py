from flask import render_template, redirect, url_for
from flask_login import login_required, current_user
from app.main import bp as main_bp
from app import login
from app import db
from app.models import Users, UserProfile

@login.user_loader
def load_user(user_id):
    from app.models import Users
    return Users.query.get(int(user_id))

@main_bp.route('/')
@main_bp.route('/index')
def index():
  return render_template('index.html', title='Главная')

@main_bp.route('/info')
def info():
    return render_template('info.html', title="Правила турнира")

@main_bp.route('/tour')
def tour():
    return render_template('tour.html', title="Турниры")
  
@main_bp.route('/personal')
@login_required
def personal():
    profile = UserProfile.query.filter_by(user_id=current_user.id).first()
    
    results = []
    
    return render_template('personal.html',
                        title='Личный кабинет',
                        profile=profile,
                        results=results,
                        is_admin=current_user.username == 'admin')