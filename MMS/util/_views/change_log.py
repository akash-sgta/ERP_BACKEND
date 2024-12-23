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
from util.functions import Custom

# =====================================================================
custom_ref = Custom()


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
        BasicAuthentication,
        JWTAuthentication,
    ]

    allowed_methods = "GET,POST,PUT,DELETE,OPTIONS".split(",")
    serializer_class = Serializer
    model = Model

    def _get_vars(self, **kwargs):
        """
        Method to get custom variables for the model.
        """
        return custom_ref.cust_get_vars(model_ref=self, **kwargs)

    def get(self, request, *args, **kwargs):
        """
        Handle GET requests to retrieve data.
        """
        return custom_ref.cust_get(model_ref=self, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests to create new data.
        """
        return custom_ref.cust_post(
            model_ref=self, data=request.data, *args, **kwargs
        )

    def put(self, request, *args, **kwargs):
        """
        Handle PUT requests to update existing data.
        """
        return custom_ref.cust_put(
            model_ref=self, data=request.data, *args, **kwargs
        )

    def delete(self, request, *args, **kwargs):
        """
        Handle DELETE requests to delete data.
        """
        return custom_ref.cust_delete(model_ref=self, *args, **kwargs)

    def options(self, request, *args, **kwargs):
        """
        Handle OPTIONS requests to provide information about the allowed HTTP methods.
        """
        return custom_ref.cust_options(
            model_ref=self, request=request, *args, **kwargs
        )
