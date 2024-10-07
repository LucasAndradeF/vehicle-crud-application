from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flasgger import Swagger
from .swagger_template import swagger_template

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config.from_object("app.config.Config")

    db.init_app(app)
    CORS(app, origins=["http://127.0.0.1:5501"])
    Swagger(app, template=swagger_template)

    with app.app_context():
        db.create_all()

    from .routes import bp

    app.register_blueprint(bp)

    return app
