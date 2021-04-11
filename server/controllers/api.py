import flask
import application

def hello():
    return flask.Response('hello', 200)