from flask_openapi3 import OpenAPI, Info
from api import api
from lib import UUIDConverter

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

if __name__ == "__main__":
    app.run()
