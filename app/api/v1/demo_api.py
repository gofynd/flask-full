import logging
from flask import jsonify
from app.tasks import task_1

logger = logging.getLogger(__name__)


def get_demo_api():
    """
     GET Demo API
     ---
    responses:
      200:
        description: Returns GET demo api response
    """
    logger.debug("in demo api")
    task_1.delay()
    return jsonify({'message': "demo get api"}), 200


def post_demo_api():
    """
     POST Demo API
     ---
    responses:
      200:
        description: Returns POST demo api response
    """
    return jsonify({'message': "demo post api"}), 200
