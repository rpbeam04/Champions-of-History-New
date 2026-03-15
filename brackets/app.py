from flask import Flask

from .routes import main_bp


def create_app(test_config=None):
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.config.from_mapping(SECRET_KEY="dev")

    if test_config:
        app.config.update(test_config)

    app.register_blueprint(main_bp)
    return app