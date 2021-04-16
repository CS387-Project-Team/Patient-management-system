import application
from flask import Flask
from application import routes
import psycopg2, config
from controllers import auth

app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.config['SECRET_KEY'] = 'thisismysecretkey'
app.register_blueprint(auth.bp)

routes.routes(app)

def connect():
    """ returns connection to database """
    conn = psycopg2.connect(database=config.name, user=config.user, password=config.pswd, host=config.host, port=config.port)
    return conn

application.connect = connect

if __name__ == "__main__":
    app.run(debug=True)