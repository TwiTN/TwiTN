from flask_openapi3 import OpenAPI, Info
from werkzeug.routing import Rule
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
    static_folder="../www/dist",
    static_url_path="/"
)
app.url_map.converters["uuid"] = UUIDConverter
app.config.from_object(__name__)

session = Session()

@app.endpoint("catch_all")
def _404(_404):
    return send_file("../www/dist/index.html")

app.url_map.add(Rule("/", defaults={"_404": ""}, endpoint="catch_all"))
app.url_map.add(Rule("/<path:_404>", endpoint="catch_all"))

app.register_api(api)
db.init_app(app)
session.init_app(app)

    
from flask import send_from_directory

@app.route('/reports/<path:path>')
def send_report(path):
    # Using request args for path will expose you to directory traversal attacks
    return send_from_directory('www/dist', path)

def create_app():

    with app.app_context():
        db.create_all()

    return app
