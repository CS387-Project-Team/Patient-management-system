from controllers import api
import application

def routes(app):
    app.add_url_rule('/hello', 'Hello world', api.hello)