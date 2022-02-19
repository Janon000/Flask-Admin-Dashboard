# This bluepint will deal with all user management functionality

from flask import Blueprint

auth = Blueprint('auth', __name__, template_folder='templates', static_folder='static')

from . import views, auth_forms
