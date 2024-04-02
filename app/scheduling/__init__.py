from flask import Blueprint

scheduling_bp = Blueprint('scheduling', __name__, template_folder='templates', static_folder='static', url_prefix='/scheduling')

from . import scheduling_rts
