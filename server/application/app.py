import application
from flask import Flask
from application import routes
import psycopg2, config, psycopg2.extras
from controllers import auth
from flask_bcrypt import Bcrypt
from flask.json import JSONEncoder
from datetime import datetime, date, time


class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        try:
            if isinstance(obj, datetime) or isinstance(obj, date) or isinstance(obj, time):
                return obj.isoformat()
            iterable = iter(obj)
        except TypeError:
            pass
        else:
            return list(iterable)
        return JSONEncoder.default(self, obj)

bcrypt = Bcrypt()

app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.config['SECRET_KEY'] = 'thisismysecretkey'
app.json_encoder = CustomJSONEncoder
app.register_blueprint(auth.bp)

bcrypt.init_app(app)
routes.routes(app)

def connect():
    """ returns connection to database """
    conn = psycopg2.connect(database=config.name, user=config.user, password=config.pswd, host=config.host, port=config.port)
    return conn

application.connect = connect
application.DictCursor = psycopg2.extras.DictCursor
application.bcrypt = bcrypt

if __name__ == "__main__":
    app.run(debug=True)