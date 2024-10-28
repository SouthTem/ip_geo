from flask import Flask
from .database import init_db, close_db

def create_app():
    app = Flask(__name__)

    with app.app_context():
        init_db()  # Initialize the database

    @app.teardown_appcontext
    def teardown_db(exception):
        close_db()

    from . import routes
    app.register_blueprint(routes.bp)

    return app
