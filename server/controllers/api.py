import flask
import application
# from flask_login import login_required, login_user, logout_user, current_user
from flask import request, make_response
from controllers.auth import login_required

@login_required
def hello():
    return flask.Response('hello', 200)

def login():
    auth = request.authorization

    if auth and auth.password == 'password':
        return flask.Response("Logged in.", 200)
    
    return make_response('Could not verify!', 401, {'WWW-Authenticate' : 'Basic realm="Login Required"'})