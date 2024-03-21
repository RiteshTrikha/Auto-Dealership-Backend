from flask import Blueprint

services_bp = Blueprint('services', __name__, template_folder='templates', static_folder='static')