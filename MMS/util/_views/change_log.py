# =====================================================================
from util._models.change_log import ChangeLog as Model
from util._serializers.change_log import ChangeLog as Serializer

from rest_framework.views import APIView
from util.functions import cust_get_vars, cust_get, cust_post, cust_put, cust_delete, cust_options

# =====================================================================


class ChangeLog(APIView):

    allowed_methods = "GET,POST,UPDATE,DELETE,OPTIONS".split(",")

    serializer_class = Serializer
    model = Model

    def _get_vars(self, **kwargs):
        return cust_get_vars(_model=self, **kwargs)

    def get(self, request, *args, **kwargs):
        return cust_get(_model=self, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return cust_post(_model=self, data=request.data, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return cust_put(_model=self, data=request.data, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return cust_delete(_model=self, *args, **kwargs)

    def options(self, request, *args, **kwargs):
        return cust_options(_model=self, request=request, *args, **kwargs)
