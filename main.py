import os
from flask_openapi3 import OpenAPI, Info
from flask import send_file
from flask_session import Session
from cachelib.file import FileSystemCache
from api import api
from db import db
from lib import UUIDConverter


SESSION_TYPE = "cachelib"
SESSION_SERIALIZATION_FORMAT = "json"
SESSION_CACHELIB = FileSystemCache(threshold=500, cache_dir="/tmp/sessions")
SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "postgresql+psycopg://postgres:9F4WF/7IhA+XRBPp@db:5432/twitn")

def create_app():
    info = Info(
        title="Twi'TN API", description="Api for Twi'TN application", version="1.0.0"
    )

    cookie = {"type": "apiKey", "in": "cookie", "name": "session_id"}
    security_schemas = {
        "api_key": cookie,
    }

    app = OpenAPI(
        __name__,
        info=info,
        security_schemes=security_schemas,
        static_folder=os.path.join(os.path.dirname(__file__), "www/dist"),
        static_url_path="/",
    )
    app.url_map.converters["uuid"] = UUIDConverter
    app.config.from_mapping({
        "SESSION_TYPE": SESSION_TYPE,
        "SESSION_SERIALIZATION_FORMAT": SESSION_SERIALIZATION_FORMAT,
        "SESSION_CACHELIB": SESSION_CACHELIB,
        "SQLALCHEMY_DATABASE_URI": SQLALCHEMY_DATABASE_URI,
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
    })

    session = Session()


    @app.errorhandler(404)
    def page_not_found(e):
        # On utilise un chemin absolu pour éviter les erreurs de dossier courant
        path_to_index = os.path.join(app.root_path, "www/dist/index.html")
        return send_file(path_to_index)


    app.register_api(api)
    db.init_app(app)
    session.init_app(app)

    return app

if __name__ == "__main__":
    application = create_app()
    application.run()
