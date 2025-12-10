from flask_openapi3 import OpenAPI
from api import api

app = OpenAPI(__name__)
app.register_api(api)

if __name__ == "__main__":
    app.run()
