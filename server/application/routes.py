from controllers import api
import application

def routes(app):
    app.add_url_rule('/hello', view_func=api.hello)
    app.add_url_rule('/dashboard', view_func=api.dashboard)