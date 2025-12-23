#!/bin/env python3

from app import app
import json

with open("openapi_spec.json", "w") as f:
    json.dump(app.api_doc, f, indent=2)