from . import hello


def register(flask_app):
    """Register APIs"""

    flask_app.register_blueprint(hello.bp, url_prefix="/api/v1")
