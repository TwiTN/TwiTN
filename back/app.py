from flask_openapi3 import OpenAPI, Info
from api import api
from db import db

info = Info(
    title="Twi'TN API",
    description="Api for Twi'TN application",
    version="1.0.0"
)

app = OpenAPI(__name__)
app.register_api(api)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql+psycopg://postgres:admin@127.0.0.1:5432/postgres"
db.init_app(app)

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run()
