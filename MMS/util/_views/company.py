# =====================================================================
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.authentication import (
    SessionAuthentication,
    BasicAuthentication,
)

from util._serializers.company import Company as Serializer
from util._models.company import Company as Model
from util._views.change_log import ChangeLog

from util.functions import Custom


# =====================================================================
custom_ref = Custom()


class Company(APIView):
    """
    Company APIView to handle CRUD operations for the Company model.

    Allowed Methods:
    - GET: Retrieve data from the Company model.
    - POST: Create new entries in the Company model.
    - PUT: Update existing entries in the Company model.
    - DELETE: Soft delete entries in the Company model.
    - OPTIONS: Provide information about the allowed HTTP methods.
    """

    permission_classes = [IsAuthenticated]
    authentication_classes = [
        SessionAuthentication,
        BasicAuthentication,
        JWTAuthentication,
    ]

    allowed_methods = "GET,POST,PUT,DELETE,OPTIONS".split(",")
    queryset = Model.objects.all()
    serializer_class = Serializer
    model = Model

    C_USER = "_user_"
    C_COMPANY = "company"

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
        try:
            company_ref = custom_ref.cust_fetch_company(
                user=request.user.username
            )
            kwargs.update({self.C_COMPANY: company_ref})
            kwargs.update({self.C_USER: request.user.username})
        except KeyError:
            pass
        return custom_ref.cust_post(
            model_ref=self, data=request.data, *args, **kwargs
        )

    def put(self, request, *args, **kwargs):
        """
        Handle PUT requests to update existing data.
        """
        # try:
        #     kwargs.update({"user": request.user.username})
        # except KeyError:
        #     pass
        return custom_ref.cust_put(
            model_ref=self, data=request.data, *args, **kwargs
        )

    def delete(self, request, *args, **kwargs):
        """
        Handle DELETE requests to delete data.
        """
        # try:
        #     kwargs.update({"user": request.user.username})
        # except KeyError:
        #     pass
        return custom_ref.cust_delete(model_ref=self, *args, **kwargs)

    def options(self, request, *args, **kwargs):
        """
        Handle OPTIONS requests to provide information about the allowed HTTP methods.
        """
        # try:
        #     kwargs.update({"user": request.user.username})
        # except KeyError:
        #     pass
        return custom_ref.cust_options(
            model_ref=self, request=request, *args, **kwargs
        )
