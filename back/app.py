from flask_openapi3 import OpenAPI, Info
from back.api import api
from back.db import db
from back.lib import UUIDConverter

info = Info(
    title="Twi'TN API", description="Api for Twi'TN application", version="1.0.0"
)

cookie = {"type": "apiKey", "in": "cookie", "name": "session_id"}
security_schemas = {
    "api_key": cookie,
}

app = OpenAPI(__name__, info=info, security_schemes=security_schemas)

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
