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
SQLALCHEMY_DATABASE_URI = "postgresql+psycopg://postgres:admin@127.0.0.1:5432/postgres"

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
    static_folder=os.path.join(os.path.dirname(__file__), "../www/dist"),
    static_url_path="/",
)
app.url_map.converters["uuid"] = UUIDConverter
app.config.from_object(__name__)

session = Session()


@app.errorhandler(404)
def page_not_found(e):
    # On utilise un chemin absolu pour éviter les erreurs de dossier courant
    path_to_index = os.path.join(app.root_path, "../www/dist/index.html")
    return send_file(path_to_index)


app.register_api(api)
db.init_app(app)
session.init_app(app)


def create_app():
    with app.app_context():
        db.create_all()

    return app
