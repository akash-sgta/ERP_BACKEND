# =====================================================================
from util._serializers.government_id_type import (
    GovernmentIdType as Serializer,
)
from util._models.government_id_type import GovernmentIdType as Model
from util._views.master import Master

# =====================================================================


class GovernmentIdType(Master):
    """
    GovernmentIdType APIView to handle CRUD operations for the GovernmentIdType model.

    Allowed Methods:
    - GET: Retrieve data from the GovernmentIdType model.
    - POST: Create new entries in the GovernmentIdType model.
    - PUT: Update existing entries in the GovernmentIdType model.
    - DELETE: Soft delete entries in the GovernmentIdType model.
    - OPTIONS: Provide information about the allowed HTTP methods.
    """

    queryset = Model.objects.all()
    serializer_class = Serializer
    model = Model
