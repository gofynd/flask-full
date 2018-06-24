from flask import Blueprint
from app.api.v1.demo_api import get_demo_api, post_demo_api

api_v1 = Blueprint('api.v1', __name__)

api_v1.add_url_rule('/demo-api/', view_func=get_demo_api, methods=['GET'])
api_v1.add_url_rule('/demo-api/', view_func=post_demo_api, methods=['POST'])
