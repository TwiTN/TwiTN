from flask_openapi3 import OpenAPI, Info
from flask_session import Session
from cachelib.file import FileSystemCache
from api import api
from db import db
from lib import UUIDConverter

SESSION_TYPE = "cachelib"
SESSION_SERIALIZATION_FORMAT = "json"
SESSION_CACHELIB = FileSystemCache(threshold=500, cache_dir="./.sessions")
SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"


def create_app(testing: bool = False):
    info = Info(
        title="Twi'TN API",
        description="Api for Twi'TN application",
        version="1.0.0",
    )

    cookie = {"type": "apiKey", "in": "cookie", "name": "session_id"}
    security_schemas = {"api_key": cookie}

    app = OpenAPI(
        __name__,
        info=info,
        security_schemes=security_schemas,
    )

    app.config.from_object(__name__)

    if testing:
        app.config["TESTING"] = True

    session = Session()

    app.url_map.converters["uuid"] = UUIDConverter

    app.register_api(api)
    db.init_app(app)
    session.init_app(app)

    with app.app_context():
        db.create_all()

    return app
