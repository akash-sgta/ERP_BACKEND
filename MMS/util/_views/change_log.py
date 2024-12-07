# =====================================================================
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.authentication import (
    SessionAuthentication,
    BasicAuthentication,
)

from util._models.change_log import ChangeLog as Model
from util._serializers.change_log import ChangeLog as Serializer
from util.functions import (
    cust_get_vars,
    cust_get,
    cust_post,
    cust_put,
    cust_delete,
    cust_options,
)

# =====================================================================


class ChangeLog(APIView):
    """
    ChangeLog APIView to handle CRUD operations for the ChangeLog model.

    Allowed Methods:
    - GET: Retrieve data from the ChangeLog model.
    - POST: Create new entries in the ChangeLog model.
    - PUT: Update existing entries in the ChangeLog model.
    - DELETE: Soft delete entries in the ChangeLog model.
    - OPTIONS: Provide information about the allowed HTTP methods.

    Attributes:
    - serializer_class: Serializer class used for validating and serializing data.
    - model: The model associated with this APIView.
    """

    permission_classes = [IsAuthenticated]
    authentication_classes = [
        SessionAuthentication,
        JWTAuthentication,
        BasicAuthentication,
    ]

    allowed_methods = "GET,POST,PUT,DELETE,OPTIONS".split(",")
    serializer_class = Serializer
    model = Model

    def _get_vars(self, **kwargs):
        """
        Method to get custom variables for the model.
        """
        return cust_get_vars(_model=self, **kwargs)

    def get(self, request, *args, **kwargs):
        """
        Handle GET requests to retrieve data.
        """
        return cust_get(_model=self, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests to create new data.
        """
        return cust_post(_model=self, data=request.data, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        """
        Handle PUT requests to update existing data.
        """
        return cust_put(_model=self, data=request.data, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """
        Handle DELETE requests to delete data.
        """
        return cust_delete(_model=self, *args, **kwargs)

    def options(self, request, *args, **kwargs):
        """
        Handle OPTIONS requests to provide information about the allowed HTTP methods.
        """
        return cust_options(_model=self, request=request, *args, **kwargs)
