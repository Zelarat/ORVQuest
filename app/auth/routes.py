from flask import render_template, redirect, url_for, flash, request, session
from flask_login import login_user, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy as sa
from urllib.parse import urlsplit
from sqlalchemy import select
from app import db
from app.auth.forms import LoginForm, RegistrationForm
from app.models import Users, UserProfile
from app.auth import bp as auth_bp

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.execute(
            select(Users).where(Users.username == form.username.data)
        ).scalar()
        if user is None or not user.check_password(form.password.data):
            flash('Неверное имя пользователя или пароль')
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('main.index')
        return redirect(next_page)
    return render_template('auth/login.html', title='Вход', form=form)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        
        if 'submit1' in request.form:
            username_exists = db.session.execute(
                select(Users).where(Users.username == form.username.data)
            ).scalar()

            if username_exists:
                flash('Это имя пользователя уже занято', 'danger')
                return render_template('auth/registration.html', form=form, step=1)

            email_exists = db.session.execute(
                sa.select(Users).where(Users.email == form.email.data)
            ).scalar()

            if email_exists:
                flash('Этот email уже зарегистрирован', 'danger')
                return render_template('auth/registration.html', form=form, step=1)

            # Если всё свободно, переходим к шагу 2
            return render_template('auth/registration.html', form=form, step=2)
        
        elif 'submit' in request.form:
            user = Users(
                username=form.username.data,
                email=form.email.data
            )
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            
            profile = UserProfile(
                user_id=user.id,
                last_name=form.second_name.data,
                first_name=form.name.data,
                middle_name=form.patronymic.data,
                workplace=form.place_of_work.data,
                position=form.position.data
            )
            db.session.add(profile)
            db.session.commit()
            
            flash('Поздравляем, вы успешно зарегистрированы!')
            return redirect(url_for('auth.login'))
    
    return render_template('auth/registration.html', title='Регистрация', form=form)

@auth_bp.route('/logout')
def logout():
    logout_user()
    session.clear()
    return redirect(url_for('main.index'))