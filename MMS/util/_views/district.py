# =====================================================================
from util._serializers.district import District as Serializer
from util._models.district import District as Model
from util._views.master import Master

# =====================================================================


class District(Master):
    """
    District APIView to handle CRUD operations for the District model.

    Allowed Methods:
    - GET: Retrieve data from the District model.
    - POST: Create new entries in the District model.
    - PUT: Update existing entries in the District model.
    - DELETE: Soft delete entries in the District model.
    - OPTIONS: Provide information about the allowed HTTP methods.
    """

    queryset = Model.objects.all()
    serializer_class = Serializer
    model = Model
