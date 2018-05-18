import logging

from flask import jsonify
from flask.views import MethodView

from app.tasks import task_1

logger = logging.getLogger(__name__)


class DemoApiView(MethodView):
    """
    """
    #@get_request.get(Model, GetApiSerializer, True, GetDemoApiHelper)
    def get(self, *args, **kwargs):
        logger.debug("in demo api")
        task_1.delay()
        return jsonify({'message': "demo get api"}), 200

    # @post_request.post(CreateUpdateApiHelper, CreateUpdateDemoAPiSerializer, True)
    def post(self):
        """
        """
        return jsonify({'name': "demo post api"}), 200
