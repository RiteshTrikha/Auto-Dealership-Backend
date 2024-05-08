from flask import Blueprint

auth_bp = Blueprint('auth', __name__, template_folder='templates', static_folder='static')

from . import customer_auth_rts, user_auth_rts
