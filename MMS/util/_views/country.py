# =====================================================================
from util._serializers.country import Country as Serializer
from util._models.country import Country as Model
from util._views.master import Master

# =====================================================================


class Country(Master):
    """
    Country APIView to handle CRUD operations for the Country model.

    Allowed Methods:
    - GET: Retrieve data from the Country model.
    - POST: Create new entries in the Country model.
    - PUT: Update existing entries in the Country model.
    - DELETE: Soft delete entries in the Country model.
    - OPTIONS: Provide information about the allowed HTTP methods.
    """

    queryset = Model.objects.all()
    serializer_class = Serializer
    model = Model
