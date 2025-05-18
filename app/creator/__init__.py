from flask import Blueprint

bp = Blueprint('creator', __name__, url_prefix='/creator')

from app.creator import routes