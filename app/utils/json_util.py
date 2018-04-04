from bson import ObjectId
from flask.json import JSONEncoder
from datetime import datetime

from marshmallow.utils import isoformat


class CustomFlaskJSONEncoder(JSONEncoder):

    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        if isinstance(obj, datetime):
            return datetime.strftime(obj, "%Y-%m-%dT%H:%M:%S")
        return JSONEncoder.default(self, obj)


class CustomJSONEncoder(JSONEncoder):

    def default(self, obj):
        if isinstance(obj, datetime):
            return isoformat(obj)
        return JSONEncoder.default(self, obj)