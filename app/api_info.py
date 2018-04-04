from app.constants import AUTH_STATES, AUTH_PERMISSIONS


API_INFO = {
    "api.v1.demo_api": {
        "get": {"state": AUTH_STATES["company"], "permission": AUTH_PERMISSIONS["view"]},
        "post": {"state": AUTH_STATES["company"], "permission": AUTH_PERMISSIONS["create_update"]}
    },
    "ping": {
        "get": "nologin"
    }
}