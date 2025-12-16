from flask_openapi3 import OpenAPI, Info
from api import api

info = Info(
    title="Twi'TN API",
    description="Api for Twi'TN application",
    version="1.0.0"
)
app = OpenAPI(__name__)
app.register_api(api)

if __name__ == "__main__":
    app.run()
