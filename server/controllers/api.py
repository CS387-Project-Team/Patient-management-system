import flask
import application
# from flask_login import login_required, login_user, logout_user, current_user
from flask import request, make_response
from controllers.auth import login_required
import controllers.dashboard

@login_required
def hello():
    return flask.Response('hello', 200)

@login_required
def dashboard():
    return controllers.dashboard.get_dashboard()