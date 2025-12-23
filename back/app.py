from flask_openapi3 import OpenAPI, Info
from flask_session import Session
from cachelib.file import FileSystemCache
from api import api
from db import db
from lib import UUIDConverter

info = Info(
    title="Twi'TN API", description="Api for Twi'TN application", version="1.0.0"
)

cookie = {"type": "apiKey", "in": "cookie", "name": "session_id"}
security_schemas = {
    "api_key": cookie,
}

app = OpenAPI(__name__, info=info, security_schemes=security_schemas)


SESSION_TYPE = "cachelib"
SESSION_SERIALIZATION_FORMAT = "json"
SESSION_CACHELIB = (FileSystemCache(threshold=500, cache_dir="/sessions"),)
app.config.from_object(__name__)

session = Session()
session.init_app(app)

app.url_map.converters["uuid"] = UUIDConverter

app.register_api(api)

app.config["SQLALCHEMY_DATABASE_URI"] = (
    "postgresql+psycopg://postgres:admin@127.0.0.1:5432/postgres"
)
db.init_app(app)

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run()
