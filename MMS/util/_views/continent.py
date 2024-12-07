# =====================================================================
from util._serializers.continent import Continent as Serializer
from util._models.continent import Continent as Model
from util._views.master import Master

# =====================================================================


class Continent(Master):
    """
    Continent APIView to handle CRUD operations for the Continent model.

    Allowed Methods:
    - GET: Retrieve data from the Continent model.
    - POST: Create new entries in the Continent model.
    - PUT: Update existing entries in the Continent model.
    - DELETE: Soft delete entries in the Continent model.
    - OPTIONS: Provide information about the allowed HTTP methods.
    """

    queryset = Model.objects.all()
    serializer_class = Serializer
    model = Model
