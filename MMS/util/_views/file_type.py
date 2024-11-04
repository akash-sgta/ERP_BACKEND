# =====================================================================
from util._serializers.file_type import FileType as Serializer
from util._models.file_type import FileType as Model
from util._views.master import Master

# =====================================================================


class FileType(Master):

    queryset = Model.objects.all()
    serializer_class = Serializer
    model = Model
