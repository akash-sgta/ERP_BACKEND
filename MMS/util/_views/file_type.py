# =====================================================================
from util._serializers.file_type import FileType as Serializer
from util._models.file_type import FileType as Model
from util._views.master import Master

# =====================================================================


class FileType(Master):
    """
    FileType APIView to handle CRUD operations for the FileType model.

    Allowed Methods:
    - GET: Retrieve data from the FileType model.
    - POST: Create new entries in the FileType model.
    - PUT: Update existing entries in the FileType model.
    - DELETE: Soft delete entries in the FileType model.
    - OPTIONS: Provide information about the allowed HTTP methods.
    """

    queryset = Model.objects.all()
    serializer_class = Serializer
    model = Model
