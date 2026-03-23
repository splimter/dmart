import json
import inspect
from fastapi.routing import APIRoute

import sys
import os

sys.path.insert(0, os.path.abspath("backend"))

from backend.main import app

routes = []
for route in app.routes:
    if isinstance(route, APIRoute):
        route_info = {
            "path": route.path,
            "methods": list(route.methods),
            "name": route.name,
        }
        routes.append(route_info)

with open("api_routes.json", "w") as f:
    json.dump(routes, f, indent=2)
