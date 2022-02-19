from . import auth

from flask import (
    render_template,
    redirect,
    flash,
    url_for,
    session,
    request,
    jsonify,
    current_app
)

from flask_login import (
    login_user,
    current_user,
    logout_user,
    login_required,
)
from datetime import timedelta
from werkzeug.routing import BuildError
from flask_bcrypt import check_password_hash
from fleetdashboard import db, login_manager, bcrypt
from fleetdashboard.models import User
from .auth_forms import login_form


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@auth.before_request
def session_handler():
    session.permanent = True
    current_app.permanent_session_lifetime = timedelta(minutes=30)


@auth.route("/login", methods=("GET", "POST"), strict_slashes=False)
def login():
    form = login_form()

    if form.validate_on_submit():
        try:
            user = User.query.filter_by(email=form.email.data).first()
            if check_password_hash(user.pwd, form.pwd.data):
                login_user(user)
                return redirect(url_for('main.dashboard'))
            else:
                flash("Invalid Username or password!", "danger")
        except Exception as e:
            flash("Invalid Username", "danger")


    return render_template("auth/login.html",
                           form=form,
                           text="Login",
                           title="Login",
                           btn_action="Login"
                           )


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('.login'))
