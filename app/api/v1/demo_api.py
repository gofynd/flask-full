import logging

from flask import jsonify
from flask.views import MethodView

logger = logging.getLogger(__name__)


class DemoApiView(MethodView):
    """
    """
    #@get_request.get(Model, GetApiSerializer, True, GetDemoApiHelper)
    def get(self, *args, **kwargs):
        return jsonify({'message': "demo get api"}), 200
        pass

    # @post_request.post(CreateUpdateApiHelper, CreateUpdateDemoAPiSerializer, True)
    def post(self):
        """
        """
        return jsonify({'name': "demo post api"}), 200
