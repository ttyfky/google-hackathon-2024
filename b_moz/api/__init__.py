from . import collect


def register(flask_app):
    """Register APIs"""

    flask_app.register_blueprint(collect.bp)
