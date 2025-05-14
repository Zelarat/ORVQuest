from flask import Blueprint

bp = Blueprint('tour', __name__, url_prefix='/tour')

from app.tour import routes