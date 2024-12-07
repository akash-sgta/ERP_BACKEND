# =====================================================================
from util._serializers.state import State as Serializer
from util._models.state import State as Model
from util._views.master import Master

# =====================================================================


class State(Master):
    """
    State APIView to handle CRUD operations for the State model.

    Allowed Methods:
    - GET: Retrieve data from the State model.
    - POST: Create new entries in the State model.
    - PUT: Update existing entries in the State model.
    - DELETE: Soft delete entries in the State model.
    - OPTIONS: Provide information about the allowed HTTP methods.
    """

    queryset = Model.objects.all()
    serializer_class = Serializer
    model = Model
