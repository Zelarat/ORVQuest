from flask import Blueprint

bp = Blueprint('creator', __name__, url_prefix='/creator')

from app.admin import routes