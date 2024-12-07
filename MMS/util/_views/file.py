# =====================================================================
from util._serializers.file import File as Serializer
from util._models.file import File as Model
from util._views.master import Master

# =====================================================================


class File(Master):
    """
    File APIView to handle CRUD operations for the File model.

    Allowed Methods:
    - GET: Retrieve data from the File model.
    - POST: Create new entries in the File model.
    - PUT: Update existing entries in the File model.
    - DELETE: Soft delete entries in the File model.
    - OPTIONS: Provide information about the allowed HTTP methods.
    """

    queryset = Model.objects.all()
    serializer_class = Serializer
    model = Model
