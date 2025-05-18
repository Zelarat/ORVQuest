import os
from dotenv import load_dotenv

load_dotenv()
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # Основные настройки
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-here'
    REMEMBER_COOKIE_DURATION = 3600  # 1 час
    
    # База данных
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Загрузка файлов
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app', 'static', 'files')
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'doc', 'docx'}