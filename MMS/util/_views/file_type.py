# =====================================================================
from util._serializers.file_type import FileType as Serializer
from util._models.file_type import FileType as Model
from util._views.change_log import ChangeLog

# =====================================================================


class FileType(ChangeLog):

    queryset = Model.objects.all()
    serializer_class = Serializer
    model = Model
