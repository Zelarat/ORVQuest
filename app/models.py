from datetime import datetime, timezone
from typing import Optional, Dict, Any
import sqlalchemy as sa
import sqlalchemy.orm as so
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from sqlalchemy.orm import validates
from app import db


class Users(db.Model, UserMixin):
    """Таблица для учетных данных"""
    __tablename__ = "users"
    
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), unique=True, nullable=False)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), unique=True, nullable=False)
    password_hash: so.Mapped[str] = so.mapped_column(sa.String(128), nullable=False)
    remember_me: so.Mapped[bool] = so.mapped_column(default=False)
    is_admin: so.Mapped[bool] = so.mapped_column(default=False)
    
    profile: so.Mapped["UserProfile"] = so.relationship(
        back_populates="user", 
        uselist=False, 
        cascade="all, delete-orphan"
    )
    
    result: so.WriteOnlyMapped["TourResult"] = so.relationship()
    user_answer: so.WriteOnlyMapped["UserAnswer"] = so.relationship()
    
    
    @validates('email')
    def validate_email(self, key, email):
        if not email or '@' not in email:
            raise ValueError("Invalid email address")
        return email
    
    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

class UserProfile(db.Model):
    """Таблица для персональных данных"""
    __tablename__ = "user_profiles"
    
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey("users.id"), unique=True, nullable=False)
    last_name: so.Mapped[str] = so.mapped_column(sa.String(64), nullable=False)
    first_name: so.Mapped[str] = so.mapped_column(sa.String(64), nullable=False)
    middle_name: so.Mapped[str] = so.mapped_column(sa.String(64))
    workplace: so.Mapped[str] = so.mapped_column(sa.String(128))
    position: so.Mapped[str] = so.mapped_column(sa.String(128))
    user: so.Mapped["Users"] = so.relationship(back_populates="profile")


#-------------------------------------------TASK-------------------------------------------

class Task(db.Model):
    __tablename__ = "task"
    
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    quest_name: so.Mapped[str] = so.mapped_column(sa.String(255), nullable=False)
    question: so.Mapped[str] = so.mapped_column(sa.Text, nullable=False)  # Текст вопроса
    task_type: so.Mapped[str] = so.mapped_column(sa.String(32), nullable=False)  # Тип задания
    points: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=False, default=1)  # Количество очков за задание
    create_at: so.Mapped[datetime] = so.mapped_column(default=datetime.now(timezone.utc), nullable=False)
    author: so.Mapped[str] = so.mapped_column(sa.String(255), nullable=False)
    
    # Connect
    options: so.Mapped["TaskOption"] = so.relationship("TaskOption", back_populates="task", uselist=False, cascade="all, delete-orphan")
    user_answer: so.Mapped["UserAnswer"] = so.relationship("UserAnswer", back_populates="task", cascade="all, delete-orphan")
    text_answer: so.Mapped["TextAnswer"] = so.relationship("TextAnswer", back_populates="task", cascade="all, delete-orphan")
    number_answer: so.Mapped["NumberAnswer"] = so.relationship("NumberAnswer", back_populates="task", uselist=False, cascade="all, delete-orphan")
    
    taskSelectedText: so.Mapped["TaskSelectedText"] = so.relationship(back_populates="task", uselist=False, cascade="all, delete-orphan") 

class TaskSelectedText(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    task_id: so.Mapped[int] = so.mapped_column(sa.Integer, sa.ForeignKey("task.id"), unique=True)
    options: so.Mapped[Optional[Dict[str, dict]]] = so.mapped_column(sa.JSON)

    task: so.Mapped["Task"] = so.relationship(back_populates="taskSelectedText")

#------------------------------------------------------------------------------------------


class TaskOption(db.Model):
    """Варианты ответов для заданий (для типов с выбором)"""
    __tablename__ = 'task_options'
    
    id: so.Mapped[int] = so.mapped_column(sa.Integer, primary_key=True)
    task_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey("task.id"), unique=True)
    options: so.Mapped[Optional[Dict[str, Any]]] = so.mapped_column(sa.JSON)
    
    # Connect
    task: so.Mapped["Task"] = so.relationship(back_populates="options")
    
class TextAnswer(db.Model):
    __tablename__ = "text_answer"
    
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    task_id: so.Mapped[int] = so.mapped_column(sa.Integer, sa.ForeignKey("task.id"), nullable=False, unique=True)
    text_answer: so.Mapped[str] = so.mapped_column(sa.Text, nullable=True)
    is_regular: so.Mapped[bool] = so.mapped_column(sa.Boolean, nullable=False)
    
    # Connect
    task: so.Mapped["Task"] = so.relationship("Task", back_populates="text_answer")

class NumberAnswer(db.Model):
    __tablename__ = "number_answer"
    
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    task_id: so.Mapped[int] = so.mapped_column(sa.Integer, sa.ForeignKey("task.id"), nullable=False, unique=True)
    answer: so.Mapped[float] = so.mapped_column(sa.Float, nullable=False)
    error_rate: so.Mapped[float] = so.mapped_column(sa.Float, nullable=False, default=0.0)
    
    # Connect
    task: so.Mapped["Task"] = so.relationship("Task", back_populates="number_answer")
    
class Tournament(db.Model):
    __tablename__ = "tournament"
    
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    tour_name: so.Mapped[str] = so.mapped_column(sa.String(255), nullable=False)
    tour_description: so.Mapped[str] = so.mapped_column(sa.Text, nullable=True)
    test_duration: so.Mapped[int] = so.mapped_column(nullable=True)
    create_at: so.Mapped[datetime] = so.mapped_column(default=datetime.now(timezone.utc))
    start_at: so.Mapped[datetime] = so.mapped_column()
    author: so.Mapped[str] = so.mapped_column(sa.String(128), nullable=False)
    
    # Connect
    tour_setting: so.Mapped["TourSetting"] = so.relationship("TourSetting", back_populates='tour', uselist=False, cascade="all, delete-orphan")
    tour_result: so.WriteOnlyMapped["TourResult"] = so.relationship(back_populates="tour")

class TourSetting(db.Model):
    __tablename__ = "tour_setting"
    
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    tour_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey("tournament.id"), unique=True)
    group: so.Mapped[Optional[Dict[str, Any]]] = so.mapped_column(sa.JSON)
    is_random: so.Mapped[bool] = so.mapped_column(sa.Boolean, default=False, nullable=False)
    count: so.Mapped[int] = so.mapped_column(sa.Integer, default=None)
    
    # Connect
    tour: so.Mapped["Tournament"] = so.relationship('Tournament', back_populates='tour_setting')
    
class TourResult(db.Model):
    __tablename__ = "tour_result"
    
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    tour_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey("tournament.id"))
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey("users.id"))
    complete_time: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=False)
    score: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=False)
    
    tour: so.Mapped["Tournament"] = so.relationship("Tournament", back_populates="tour_result")
    user: so.Mapped["Users"] = so.relationship("Users", back_populates="result")
    
class UserAnswer(db.Model):
    __tablename__ = "user_answer"
    
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    score: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=False)
    answer: so.Mapped[str] = so.mapped_column(sa.String(255), nullable=True)
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey("users.id"))
    task_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey("task.id"))
    
    # Connect
    task: so.Mapped["Task"] = so.relationship("Task", back_populates="user_answer")
    user: so.Mapped["Users"] = so.relationship("Users", back_populates="user_answer")
