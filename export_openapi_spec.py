#!/bin/env python3

from main import create_app
import json

with open("openapi_spec.json", "w") as f:
    json.dump(create_app().api_doc, f, indent=2)
