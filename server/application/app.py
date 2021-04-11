import application
from flask import Flask
from application import routes
app = Flask(__name__)

routes.routes(app)


if __name__ == "__main__":
    app.run(debug=True)